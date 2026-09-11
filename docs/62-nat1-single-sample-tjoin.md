# 62 — NAT1 single-sample multi-error T-join negative control

## Status

**NAT1 is a falsification experiment in progress.** It removes both NAT0 conveniences: there is exactly one noisy public sample and the error set contains multiple independently selected public edges without separation conditioning.

NAT1 is not a KEM, one-way function, post-quantum assumption, or production-security construction.

## Carrier

NAT1 reuses the constructive flip-mixed sphere machinery from G15 only as a public sparse complex. The carrier starts from an icosahedral sphere, grows to the requested size, performs a deterministic legal edge-flip walk, and is globally relabelled.

Toy sets:

```text
nat1-36: F=36, 360 successful flips, t in {1,2,3,4}
nat1-54: F=54, 540 successful flips, t in {1,2,3,4,5}
nat1-72: F=72, 720 successful flips, t in {1,2,3,4,5,6}
```

The sphere choice is deliberate for this gate. `H^1(S^2; F2)=0`, so once an attacker finds any public error set with the observed triangle syndrome, subtracting it leaves a public coboundary rather than an unresolved homology sector. NAT1 therefore isolates the noise-decoding question cleanly.

## Noisy relation

A hidden vertex 0-cochain induces a clean public edge coboundary. Generation chooses `t` distinct public edges by a deterministic uniform-style seeded ordering and flips exactly those bits. Only one observed edge vector is published.

There is no repeated-sample majority, no enforced spacing between errors, and no hidden reference requirement in recovery.

## NAT-A002 — public minimum T-join decoding

On a closed triangulated surface, every noisy primal edge corresponds to one dual edge joining the two incident triangles. The odd triangle parities are therefore exactly the boundary defects of the dual error subgraph.

The public attacker:

1. computes all violated triangle parities;
2. builds the public dual graph;
3. runs BFS from each defect to obtain all defect-pair distances and canonical shortest paths;
4. solves the exact minimum perfect pairing of defects by bitmask dynamic programming;
5. XORs the selected shortest paths to obtain a minimum T-join correction;
6. removes that correction from the observed edge data;
7. reconstructs a public vertex assignment from the resulting coboundary;
8. verifies the clean coboundary directly.

Any accepted clean object is attacker success. The recovered correction need not equal the planted error set and the recovered normalized vertex assignment need not equal the planted one.

## Measurements

Record at least:

- public `V/E/F`;
- planted public noise weight `t`;
- syndrome/defect weight;
- defect-root BFS count, queue pops and edge scans;
- exact matching-DP state count and pair tests;
- minimum matching/T-join distance;
- recovered error weight;
- exact public clean-object acceptance;
- post-success equality with planted noise and normalized hidden vertex assignment;
- deterministic curve over all declared `t` values and multi-seed sweep.

## Rejection gate

Reject NAT1 if exact public graph decoding routinely produces an accepted clean object over the declared toy noise range with small work. A different minimum correction is still a break.

Do not repair by increasing only `t` while the relation remains a public surface T-join problem. A successor must change the noisy relation so its residual uncertainty is not equivalent to ordinary defect matching on a public dual graph.

No security claim.
