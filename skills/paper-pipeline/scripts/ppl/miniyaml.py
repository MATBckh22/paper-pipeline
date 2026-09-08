"""Fallback YAML loader for the paper-config subset.

Used only when PyYAML is not importable. Supports exactly the subset the
paper-config schema documents: block mappings, block sequences, flow lists of
scalars, single/double-quoted and plain scalars, comments. Anchors, aliases,
multiline scalars, and flow mappings are outside the subset and raise
MiniYamlError with the offending line number.
"""

import re

__all__ = ["load", "MiniYamlError"]


class MiniYamlError(ValueError):
    def __init__(self, message, lineno):
        super().__init__("line %d: %s" % (lineno, message))
        self.lineno = lineno


_INT_RE = re.compile(r"^-?\d+$")
_FLOAT_RE = re.compile(r"^-?\d+\.\d+([eE][+-]?\d+)?$")
# key: rest -- key is plain (no quotes needed for our subset)
_KEY_RE = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9_ .\-]*):(?:\s+(.*))?$")


def _strip_comment(text):
    """Remove a trailing comment that is outside quotes."""
    out = []
    quote = None
    for i, ch in enumerate(text):
        if quote:
            if ch == quote:
                quote = None
            out.append(ch)
        elif ch in "'\"":
            quote = ch
            out.append(ch)
        elif ch == "#" and (i == 0 or text[i - 1] in " \t"):
            break
        else:
            out.append(ch)
    return "".join(out).rstrip()


def _scalar(text, lineno):
    text = text.strip()
    if text.startswith("[") and text.endswith("]"):
        return _flow_list(text[1:-1], lineno)
    if text.startswith("{"):
        raise MiniYamlError("flow mappings are outside the subset", lineno)
    if text.startswith("&") or text.startswith("*"):
        raise MiniYamlError("anchors/aliases are outside the subset", lineno)
    if text.startswith("|") or text.startswith(">"):
        raise MiniYamlError("multiline scalars are outside the subset", lineno)
    if (text.startswith('"') and text.endswith('"') and len(text) >= 2) or (
        text.startswith("'") and text.endswith("'") and len(text) >= 2
    ):
        return text[1:-1]
    if text in ("null", "~", ""):
        return None
    if text == "true":
        return True
    if text == "false":
        return False
    if _INT_RE.match(text):
        return int(text)
    if _FLOAT_RE.match(text):
        return float(text)
    return text


def _flow_list(body, lineno):
    items, buf, quote = [], [], None
    for ch in body:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
            buf.append(ch)
        elif ch == ",":
            items.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if quote:
        raise MiniYamlError("unterminated quote in flow list", lineno)
    items.append("".join(buf))
    items = [s.strip() for s in items]
    if items == [""]:
        return []
    return [_scalar(s, lineno) for s in items]


def _lines(text):
    """Yield (indent, content, lineno) for significant lines."""
    rows = []
    for n, raw in enumerate(text.splitlines(), 1):
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise MiniYamlError("tabs are not allowed in indentation", n)
        stripped = _strip_comment(raw)
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        rows.append((indent, stripped.strip(), n))
    return rows


def _parse_block(rows, i, indent):
    """Parse a block (mapping or sequence) whose entries sit at `indent`."""
    if rows[i][1].startswith("- ") or rows[i][1] == "-":
        return _parse_seq(rows, i, indent)
    return _parse_map(rows, i, indent)


def _parse_map(rows, i, indent):
    result = {}
    while i < len(rows):
        ind, content, lineno = rows[i]
        if ind < indent:
            break
        if ind > indent:
            raise MiniYamlError("unexpected indentation", lineno)
        if content.startswith("- "):
            raise MiniYamlError("sequence item inside mapping block", lineno)
        m = _KEY_RE.match(content)
        if not m:
            raise MiniYamlError("expected 'key: value'", lineno)
        key, rest = m.group(1).strip(), m.group(2)
        if key in result:
            raise MiniYamlError("duplicate key %r" % key, lineno)
        if rest is not None and rest.strip():
            result[key] = _scalar(rest, lineno)
            i += 1
        else:
            # value is a nested block (or empty -> None)
            if i + 1 < len(rows) and rows[i + 1][0] > indent:
                value, i = _parse_block(rows, i + 1, rows[i + 1][0])
                result[key] = value
            else:
                result[key] = None
                i += 1
    return result, i


def _parse_seq(rows, i, indent):
    result = []
    while i < len(rows):
        ind, content, lineno = rows[i]
        if ind < indent:
            break
        if ind > indent:
            raise MiniYamlError("unexpected indentation", lineno)
        if not (content.startswith("- ") or content == "-"):
            break
        body = content[2:].strip() if content.startswith("- ") else ""
        if not body:
            # nested block under a bare dash
            if i + 1 < len(rows) and rows[i + 1][0] > indent:
                value, i = _parse_block(rows, i + 1, rows[i + 1][0])
                result.append(value)
            else:
                result.append(None)
                i += 1
            continue
        m = _KEY_RE.match(body)
        if m:
            # mapping starting inline on the dash line; its keys sit at the
            # column where `body` starts (indent + 2)
            item_indent = indent + 2
            virtual = [(item_indent, body, lineno)]
            j = i + 1
            while j < len(rows) and rows[j][0] >= item_indent and not (
                rows[j][0] == indent
            ):
                virtual.append(rows[j])
                j += 1
            value, consumed = _parse_map(virtual, 0, item_indent)
            if consumed != len(virtual):
                bad = virtual[consumed]
                raise MiniYamlError("unparsed content in sequence item", bad[2])
            result.append(value)
            i = j
        else:
            result.append(_scalar(body, lineno))
            i += 1
    return result, i


def load(text):
    rows = _lines(text)
    if not rows:
        return {}
    if rows[0][0] != 0:
        raise MiniYamlError("document must start at column 0", rows[0][2])
    value, i = _parse_block(rows, 0, 0)
    if i != len(rows):
        raise MiniYamlError("unparsed trailing content", rows[i][2])
    return value
