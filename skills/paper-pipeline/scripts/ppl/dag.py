"""Outline DAG validation and figure<->claim reconciliation.

A section's `inputs` are edges to what it assumes: frame artifacts (always
available, no order) or earlier sections. Checks:
  - order violations: an input resolving to a section at higher document
    order (forward reference), reported per edge with remedies decided by the
    calling skill (reorder or restate);
  - cycles: reported as full paths, not single edges;
  - transitive blast radius: for each violating edge, every section whose
    dependency cone includes it - a pairwise-only report would leave those
    sections silently planned against a broken assumption.
"""

import collections

DagReport = collections.namedtuple(
    "DagReport", "order_violations cycles unknown_inputs transitively_affected")
FigureReport = collections.namedtuple("FigureReport", "orphan_figures prose_only_claims")


def _section_ids(sections):
    return [str(s.get("id")) for s in sections]


def check(sections, frame_artifacts=()):
    ids = _section_ids(sections)
    order = {sid: i for i, sid in enumerate(ids)}
    frame_names = set(map(str, frame_artifacts))
    deps = {}  # sid -> [input section ids]
    unknown, violations = [], []

    for s in sections:
        sid = str(s.get("id"))
        deps[sid] = []
        for inp in (s.get("inputs") or []):
            inp = str(inp)
            if inp in frame_names:
                continue
            if inp not in order:
                unknown.append((sid, inp))
                continue
            deps[sid].append(inp)
            if order[inp] >= order[sid]:
                violations.append((sid, inp))

    # cycles: DFS with colors, recover full path
    cycles = []
    color = {sid: 0 for sid in ids}  # 0 white 1 grey 2 black
    stack = []

    def dfs(u):
        color[u] = 1
        stack.append(u)
        for v in deps.get(u, []):
            if color[v] == 1:
                cycles.append(stack[stack.index(v):] + [v])
            elif color[v] == 0:
                dfs(v)
        stack.pop()
        color[u] = 2

    for sid in ids:
        if color[sid] == 0:
            dfs(sid)

    # reverse reachability: who depends (transitively) on the source of each
    # violating edge
    rdeps = collections.defaultdict(set)  # sid -> direct dependents
    for sid, ins in deps.items():
        for inp in ins:
            rdeps[inp].add(sid)

    def dependents_of(root):
        seen, todo = set(), [root]
        while todo:
            cur = todo.pop()
            for nxt in rdeps.get(cur, ()):
                if nxt not in seen:
                    seen.add(nxt)
                    todo.append(nxt)
        return seen

    affected = {}
    for sid, inp in violations:
        affected[(sid, inp)] = sorted({sid} | dependents_of(sid),
                                      key=lambda x: order.get(x, 0))

    return DagReport(violations, cycles, unknown, affected)


def figure_check(figures, sections):
    """Bipartite figures x claims. Degree-0 figure -> error (decoration);
    section whose claim rides on prose alone -> warning (legitimate, noted)."""
    referenced = set()
    prose_only = []
    for s in sections:
        figs = [str(f) for f in (s.get("figures") or [])]
        referenced.update(figs)
        if not figs:
            prose_only.append(str(s.get("id")))
    orphans = []
    for f in figures or []:
        fid = str(f.get("id"))
        if not f.get("supports_claim") or fid not in referenced:
            orphans.append(fid)
    return FigureReport(orphans, prose_only)
