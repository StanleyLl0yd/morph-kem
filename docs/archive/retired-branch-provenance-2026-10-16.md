# Retired divergent Git branch provenance (2026-10-16)

This is a **research-history preservation manifest**, not an active workstream, security finding, new experimental batch or stage allocation. When the one-time [archive workflow](../../.github/workflows/archive-legacy-branches.yml) succeeds, each legacy branch is deleted **only after** a lightweight Git tag is created **and independently re-read** pointing to the exact listed old branch-head commit. Both the archived tag and the SHA retain its *full historical tree and commit ancestry* in Git. A replacement merged PR can have a scientifically corresponding conclusion while differing in code or proof detail.

| Retired branch | Exact historical commit | Immutable archive tag (intended, verify in GitHub) | Context |
| --- | --- | --- | --- |
| `g1/hges-cycle-gluing` | [`a930b26827c3`](https://github.com/StanleyLl0yd/morph-kem/commit/a930b26827c3f6a2d337af791eabe8f43e6154ba) | `archive/2026-10-16/g1/hges-cycle-gluing` | #58 closed unmerged; canonical #61 |
| `g14/stacked-sphere-reverse-normalization` | [`bf3f35ef1f36`](https://github.com/StanleyLl0yd/morph-kem/commit/bf3f35ef1f36e4368b52235a7c2b1d39ddfb94d8) | `archive/2026-10-16/g14/stacked-sphere-reverse-normalization` | #91 closed unmerged; canonical #89 |
| `hga1/markoff-navigation-control` | [`77a1d11bb4da`](https://github.com/StanleyLl0yd/morph-kem/commit/77a1d11bb4da93799f3274d6a2ef265ac3bc555b) | `archive/2026-10-16/hga1/markoff-navigation-control` | no PR; divergent historical prototype |
| `hga4f/adaptive-representation-ensemble` | [`0ec0fe347646`](https://github.com/StanleyLl0yd/morph-kem/commit/0ec0fe3476464028399fbdf74cdbae2b6c084220) | `archive/2026-10-16/hga4f/adaptive-representation-ensemble` | #159 closed unmerged; clean #160 |
| `nat7/public-tree-gauge-normalization-clean` | [`bd9a8cd959a5`](https://github.com/StanleyLl0yd/morph-kem/commit/bd9a8cd959a50e75e17365485645b946cf6a8f0d) | `archive/2026-10-16/nat7/public-tree-gauge-normalization-clean` | no PR; divergent historical prototype |
| `research/n1-56-57-no-go-20261014` | [`bdd26a26d4ba`](https://github.com/StanleyLl0yd/morph-kem/commit/bdd26a26d4baec950d39b13cb055ac3638385ba1) | `archive/2026-10-16/research/n1-56-57-no-go-20261014` | #202 closed unmerged; #203/#205 document distinct historical proof labels |
| `tdc2f/rank-matched-kernel-control` | [`27824f521b5d`](https://github.com/StanleyLl0yd/morph-kem/commit/27824f521b5d813211b7df3a18c3511604e43c48) | `archive/2026-10-16/tdc2f/rank-matched-kernel-control` | #151 closed unmerged; clean #154 |
| `tdc3/matched-decoder-work` | [`0dda0e1eb023`](https://github.com/StanleyLl0yd/morph-kem/commit/0dda0e1eb023424ef0d4d4f01d7674b2163eeb56) | `archive/2026-10-16/tdc3/matched-decoder-work` | #169 closed unmerged; clean #170 |

The list was independently compared against `main=7f2540fd07c3d63c09939e2b3a1b143a49ce4745` before archiving: **all eight** branch tips had unique commits not reachable from `main`; **two** were no-PR historical branches, **six** were closed-unmerged PR sources. Do **not** imply byte-for-byte equivalence to current merged code. The archival action does not merge or execute experimental branches. Even abandoned/negative results remain available by exact Git SHA.

The one-time deletion is intentionally limited to the eight exact pairs. Each branch name, SHA, GitHub protection state and absence of open PRs is re-checked; any unexpected movement or tag mismatch **halts without deleting that branch**. The tags are never force-updated. Repeated execution is safe only when a branch is already missing **and the expected archived tag is present**.

Current research remains **GLOBAL NO NOMINATION**; H-A/H-B/H-C HOLD. N1-60 unallocated; original any-witness verifier and positive Field 15 admission still required. No research results, historical counts, or primitive security claims changed.
