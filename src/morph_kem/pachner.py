from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations, product
import hashlib
import json
import math
from statistics import mean

Tet = tuple[int, int, int, int]
Facets = tuple[Tet, ...]


class PachnerExperimentError(ValueError):
    """Invalid T0 bounded-Pachner experiment input."""


@dataclass(frozen=True, slots=True)
class PachnerParameters:
    name: str
    burn_in_14: int
    challenge_length: int

    def validate(self) -> None:
        if not 1 <= self.burn_in_14 <= 6 or not 1 <= self.challenge_length <= 16:
            raise PachnerExperimentError("T0 parameters outside toy bounds")


PACHNER_PARAMETER_SETS = {
    "t0-4": PachnerParameters("t0-4", 4, 4),
    "t0-6": PachnerParameters("t0-6", 4, 6),
    "t0-8": PachnerParameters("t0-8", 4, 8),
}


@dataclass(frozen=True, slots=True)
class PachnerMove:
    kind: str
    primary: tuple[int, ...]
    secondary: tuple[int, ...]

    def __post_init__(self) -> None:
        expected = {"23": (3, 2), "32": (2, 3)}.get(self.kind)
        if expected is None or (len(self.primary), len(self.secondary)) != expected:
            raise PachnerExperimentError("invalid 2-3/3-2 descriptor")
        if self.primary != tuple(sorted(self.primary)) or self.secondary != tuple(sorted(self.secondary)):
            raise PachnerExperimentError("move simplices must be canonical")

    @property
    def support(self) -> tuple[int, ...]:
        return tuple(sorted(set(self.primary) | set(self.secondary)))


def _norm(facets) -> Facets:
    out = tuple(sorted(tuple(sorted(tet)) for tet in facets))
    if any(len(tet) != 4 or len(set(tet)) != 4 for tet in out) or len(set(out)) != len(out):
        raise PachnerExperimentError("invalid tetrahedron set")
    return out


def _closed(facets: Facets) -> None:
    inc: dict[tuple[int, int, int], list[int]] = defaultdict(list)
    for i, tet in enumerate(facets):
        for face in combinations(tet, 3):
            inc[face].append(i)
    if not facets or any(len(owner) != 2 for owner in inc.values()):
        raise PachnerExperimentError("state is not a closed 3-pseudomanifold")
    adj = [set() for _ in facets]
    for a, b in inc.values():
        adj[a].add(b); adj[b].add(a)
    seen, stack = {0}, [0]
    while stack:
        for nxt in adj[stack.pop()]:
            if nxt not in seen:
                seen.add(nxt); stack.append(nxt)
    if len(seen) != len(facets):
        raise PachnerExperimentError("dual graph is disconnected")


@dataclass(frozen=True, slots=True)
class PachnerState:
    facets: Facets

    def __post_init__(self) -> None:
        if _norm(self.facets) != self.facets:
            raise PachnerExperimentError("facets are not canonical")
        _closed(self.facets)

    @property
    def vertices(self) -> tuple[int, ...]:
        return tuple(sorted({v for tet in self.facets for v in tet}))

    @property
    def tetrahedra(self) -> int:
        return len(self.facets)

    @property
    def edges(self) -> tuple[tuple[int, int], ...]:
        return tuple(sorted({edge for tet in self.facets for edge in combinations(tet, 2)}))

    @property
    def triangles(self) -> tuple[tuple[int, int, int], ...]:
        return tuple(sorted({face for tet in self.facets for face in combinations(tet, 3)}))

    @property
    def euler_characteristic(self) -> int:
        return len(self.vertices) - len(self.edges) + len(self.triangles) - len(self.facets)


@dataclass(frozen=True, slots=True)
class PachnerPublicInstance:
    parameters: PachnerParameters
    start: PachnerState
    target: PachnerState
    bound: int

    def __post_init__(self) -> None:
        self.parameters.validate()
        if self.bound != self.parameters.challenge_length:
            raise PachnerExperimentError("public bound mismatch")
        for state in (self.start, self.target):
            if state.vertices != tuple(range(len(state.vertices))):
                raise PachnerExperimentError("public endpoints must be canonical")

    def encode(self) -> bytes:
        payload = {
            "bound": self.bound,
            "params": [self.parameters.name, self.parameters.burn_in_14, self.parameters.challenge_length],
            "start": self.start.facets,
            "target": self.target.facets,
            "version": 1,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")


@dataclass(frozen=True, slots=True)
class PachnerReference:
    planted_moves: tuple[PachnerMove, ...]


@dataclass(frozen=True, slots=True)
class PachnerSearchResult:
    found: bool
    moves: tuple[PachnerMove, ...]
    distance: int | None
    visited_states: int
    expanded_states: int
    max_frontier: int


@dataclass(frozen=True, slots=True)
class PachnerBidirectionalResult:
    found: bool
    moves: tuple[PachnerMove, ...]
    distance: int | None
    forward_visited: int
    reverse_visited: int
    expanded_states: int
    max_forward_frontier: int
    max_reverse_frontier: int


@dataclass(frozen=True, slots=True)
class PachnerPathMetrics:
    planted_length: int
    initial_branching: int
    min_branching: int
    max_branching: int
    mean_branching: float
    mean_unique_branching: float
    move_23: int
    move_32: int
    neighbor_collisions: int
    commuting_pairs_tested: int
    commuting_pairs: int


class _Rng:
    def __init__(self, seed: bytes):
        self.seed, self.counter = seed, 0

    def randbelow(self, n: int) -> int:
        limit = (1 << 256) - ((1 << 256) % n)
        while True:
            block = hashlib.sha256(b"MORPH-KEM T0 rng v1\0" + self.seed + self.counter.to_bytes(8, "big")).digest()
            self.counter += 1
            value = int.from_bytes(block, "big")
            if value < limit:
                return value % n


def boundary_of_4_simplex() -> PachnerState:
    return PachnerState(tuple(combinations(range(5), 4)))


def _color_classes(facets: Facets) -> tuple[tuple[int, ...], ...]:
    vertices = tuple(sorted({v for tet in facets for v in tet})); n = len(vertices)
    pos = {v: i for i, v in enumerate(vertices)}
    tetdeg = [0] * n; codeg = [[0] * n for _ in range(n)]
    for tet in facets:
        ids = [pos[v] for v in tet]
        for i in ids: tetdeg[i] += 1
        for i, j in combinations(ids, 2): codeg[i][j] += 1; codeg[j][i] += 1
    sig = [(tetdeg[i], tuple(sorted(x for x in codeg[i] if x))) for i in range(n)]
    palette = {x: i for i, x in enumerate(sorted(set(sig)))}; colors = [palette[x] for x in sig]
    for _ in range(n + 1):
        sig = [(colors[i], tuple(sorted((colors[j], codeg[i][j]) for j in range(n) if codeg[i][j]))) for i in range(n)]
        palette = {x: i for i, x in enumerate(sorted(set(sig)))}; nxt = [palette[x] for x in sig]
        if nxt == colors: break
        colors = nxt
    return tuple(tuple(vertices[i] for i, c in enumerate(colors) if c == target) for target in sorted(set(colors)))


@lru_cache(maxsize=100_000)
def canonical_facets(facets: Facets) -> Facets:
    facets = _norm(facets); classes = _color_classes(facets)
    residual = math.prod(math.factorial(len(group)) for group in classes)
    if residual > 2_000_000:
        raise PachnerExperimentError("exact toy canonicalization residual too large")
    blocks, offset = [], 0
    for group in classes:
        blocks.append(tuple(range(offset, offset + len(group)))); offset += len(group)
    best = None
    for orders in product(*(permutations(group) for group in classes)):
        mapping = {source: target for order, block in zip(orders, blocks) for source, target in zip(order, block)}
        mapped = tuple(sorted(tuple(sorted(mapping[v] for v in tet)) for tet in facets))
        if best is None or mapped < best: best = mapped
    assert best is not None
    return best


def canonical_state(state: PachnerState) -> PachnerState:
    return PachnerState(canonical_facets(state.facets))


def _one_four(state: PachnerState, tet: Tet) -> PachnerState:
    facets = set(state.facets); facets.remove(tet); new = max(state.vertices) + 1
    for face in combinations(tet, 3): facets.add(tuple(sorted((*face, new))))
    return canonical_state(PachnerState(_norm(facets)))


def legal_moves(state: PachnerState) -> tuple[PachnerMove, ...]:
    triinc: dict[tuple[int, int, int], list[Tet]] = defaultdict(list)
    edgeinc: dict[tuple[int, int], list[Tet]] = defaultdict(list)
    edges = set(state.edges); triangles = set(state.triangles)
    for tet in state.facets:
        for face in combinations(tet, 3): triinc[face].append(tet)
        for edge in combinations(tet, 2): edgeinc[edge].append(tet)
    out: list[PachnerMove] = []
    for face, owners in triinc.items():
        if len(owners) != 2: continue
        opp = tuple(sorted(next(iter(set(tet) - set(face))) for tet in owners))
        if len(set(opp)) == 2 and opp not in edges: out.append(PachnerMove("23", face, opp))
    for edge, owners in edgeinc.items():
        if len(owners) != 3: continue
        link = tuple(sorted({v for tet in owners for v in tet} - set(edge)))
        if len(link) != 3 or link in triangles: continue
        a, b, c = link; d, e = edge
        expected = {tuple(sorted(x)) for x in ((a,b,d,e),(a,c,d,e),(b,c,d,e))}
        if set(owners) == expected: out.append(PachnerMove("32", edge, link))
    return tuple(sorted(out, key=lambda m: (m.kind, m.primary, m.secondary)))


def apply_move(state: PachnerState, move: PachnerMove) -> PachnerState:
    if move not in legal_moves(state): raise PachnerExperimentError("illegal T0 move")
    facets = set(state.facets)
    if move.kind == "23":
        face = move.primary; d, e = move.secondary
        for tet in tuple(facets):
            if set(face).issubset(tet): facets.remove(tet)
        a, b, c = face
        facets.update(tuple(sorted(x)) for x in ((a,b,d,e),(a,c,d,e),(b,c,d,e)))
    else:
        edge = move.primary; a, b, c = move.secondary; d, e = edge
        for tet in tuple(facets):
            if set(edge).issubset(tet): facets.remove(tet)
        facets.update((tuple(sorted((a,b,c,d))), tuple(sorted((a,b,c,e)))))
    return canonical_state(PachnerState(_norm(facets)))


def unique_neighbors(state: PachnerState) -> tuple[tuple[PachnerMove, PachnerState], ...]:
    by_state: dict[Facets, PachnerMove] = {}
    for move in legal_moves(state): by_state.setdefault(apply_move(state, move).facets, move)
    return tuple((by_state[key], PachnerState(key)) for key in sorted(by_state))


def _rich_burn_in(steps: int) -> PachnerState:
    level = {boundary_of_4_simplex().facets: boundary_of_4_simplex()}
    for _ in range(steps):
        nxt: dict[Facets, PachnerState] = {}
        for state in level.values():
            for tet in state.facets:
                candidate = _one_four(state, tet); nxt[candidate.facets] = candidate
        level = nxt
    return max(level.values(), key=lambda state: (len(unique_neighbors(state)), state.facets))


def generate_pachner_instance(params: PachnerParameters, master_seed: bytes) -> tuple[PachnerPublicInstance, PachnerReference]:
    params.validate()
    if not master_seed: raise PachnerExperimentError("master seed required")
    start = _rich_burn_in(params.burn_in_14); current = start; seen = {start.facets}; planted = []
    rng = _Rng(hashlib.sha256(b"MORPH-KEM T0 challenge v1\0" + params.name.encode() + b"\0" + master_seed).digest())
    for _ in range(params.challenge_length):
        candidates = [(move, target) for move, target in unique_neighbors(current) if target.facets not in seen]
        if not candidates: raise PachnerExperimentError("challenge walk dead end")
        scores = [len(unique_neighbors(target)) for _, target in candidates]; best = max(scores)
        preferred = [x for x, score in zip(candidates, scores) if score >= best - 1]
        move, current = preferred[rng.randbelow(len(preferred))]; planted.append(move); seen.add(current.facets)
    public = PachnerPublicInstance(params, start, current, params.challenge_length); reference = PachnerReference(tuple(planted))
    if not verify_pachner_witness(public, reference.planted_moves): raise PachnerExperimentError("planted path failed")
    return public, reference


def verify_pachner_witness(public: PachnerPublicInstance, moves: tuple[PachnerMove, ...]) -> bool:
    if len(moves) > public.bound: return False
    current = public.start
    try:
        for move in moves: current = apply_move(current, move)
    except PachnerExperimentError:
        return False
    return current.facets == public.target.facets


def bfs_pachner_recover(public: PachnerPublicInstance, max_states: int = 100_000) -> PachnerSearchResult:
    start, target = public.start, public.target
    parent: dict[Facets, tuple[Facets, PachnerMove] | None] = {start.facets: None}; depth = {start.facets: 0}
    queue = deque([start]); expanded = 0; max_frontier = 1
    while queue:
        current = queue.popleft(); d = depth[current.facets]
        if d >= public.bound: continue
        expanded += 1
        for move, neighbor in unique_neighbors(current):
            key = neighbor.facets
            if key in parent: continue
            if len(parent) >= max_states: return PachnerSearchResult(False, (), None, len(parent), expanded, max_frontier)
            parent[key] = (current.facets, move); depth[key] = d + 1
            if key == target.facets:
                moves = []
                while parent[key] is not None:
                    key, move = parent[key]; moves.append(move)
                moves.reverse(); return PachnerSearchResult(True, tuple(moves), len(moves), len(parent), expanded, max_frontier)
            queue.append(neighbor)
        max_frontier = max(max_frontier, len(queue))
    return PachnerSearchResult(False, (), None, len(parent), expanded, max_frontier)


def _move_between(left: PachnerState, right: PachnerState) -> PachnerMove:
    for move, target in unique_neighbors(left):
        if target.facets == right.facets: return move
    raise PachnerExperimentError("broken state path")


def bidirectional_pachner_recover(public: PachnerPublicInstance, max_states: int = 100_000) -> PachnerBidirectionalResult:
    start, target = public.start, public.target
    fp: dict[Facets, Facets | None] = {start.facets: None}; rp: dict[Facets, Facets | None] = {target.facets: None}
    fd, rd = {start.facets: 0}, {target.facets: 0}; ff, rf = {start.facets}, {target.facets}
    expanded = 0; maxf = maxr = 1; meet = None
    while ff and rf and len(fp) + len(rp) < max_states:
        forward = len(ff) <= len(rf); front = ff if forward else rf; parents = fp if forward else rp; depths = fd if forward else rd; other = rp if forward else fp
        nxt = set()
        for key in sorted(front):
            if depths[key] >= public.bound: continue
            expanded += 1
            for _, neighbor in unique_neighbors(PachnerState(key)):
                nkey = neighbor.facets
                if nkey in parents: continue
                parents[nkey] = key; depths[nkey] = depths[key] + 1
                if nkey in other and depths[nkey] + (rd[nkey] if forward else fd[nkey]) <= public.bound:
                    meet = nkey; break
                nxt.add(nkey)
            if meet is not None: break
        if forward: ff = nxt; maxf = max(maxf, len(ff))
        else: rf = nxt; maxr = max(maxr, len(rf))
        if meet is not None: break
    if meet is None: return PachnerBidirectionalResult(False, (), None, len(fp), len(rp), expanded, maxf, maxr)
    left, cursor = [], meet
    while cursor is not None: left.append(cursor); cursor = fp[cursor]
    left.reverse(); right, cursor = [], rp[meet]
    while cursor is not None: right.append(cursor); cursor = rp[cursor]
    states = tuple(PachnerState(key) for key in left + right); moves = tuple(_move_between(a, b) for a, b in zip(states, states[1:]))
    if not verify_pachner_witness(public, moves): raise PachnerExperimentError("bidir reconstruction failed")
    return PachnerBidirectionalResult(True, moves, len(moves), len(fp), len(rp), expanded, maxf, maxr)


def _commutes(state: PachnerState, left: PachnerMove, right: PachnerMove) -> bool:
    try:
        a = apply_move(state, left); candidates = [m for m in legal_moves(a) if m.kind == right.kind and m.support == right.support]
        if not candidates: return False
        lr = apply_move(a, candidates[0]); b = apply_move(state, right); candidates = [m for m in legal_moves(b) if m.kind == left.kind and m.support == left.support]
        return bool(candidates) and apply_move(b, candidates[0]).facets == lr.facets
    except PachnerExperimentError:
        return False


def pachner_path_metrics(public: PachnerPublicInstance, reference: PachnerReference) -> PachnerPathMetrics:
    state = public.start; branching = []; unique = []; collisions = tested = commuting = 0
    for planted in reference.planted_moves:
        moves = legal_moves(state); neighbors = unique_neighbors(state); branching.append(len(moves)); unique.append(len(neighbors)); collisions += len(moves) - len(neighbors)
        for left, right in combinations(moves, 2): tested += 1; commuting += int(_commutes(state, left, right))
        state = apply_move(state, planted)
    return PachnerPathMetrics(len(reference.planted_moves), branching[0], min(branching), max(branching), mean(branching), mean(unique), sum(m.kind == "23" for m in reference.planted_moves), sum(m.kind == "32" for m in reference.planted_moves), collisions, tested, commuting)
