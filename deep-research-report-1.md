# Symbolic Regression as a Compression Engine

Your intuition from that Riemann screenshot is pointing at something real. The panel is visualizing Riemann’s explicit formula: a jagged, discrete arithmetic object is rewritten as a smooth main term plus oscillatory corrections indexed by the nontrivial zeros of the zeta function. That is exactly the kind of representation shift that compression exploits. The mathematically honest version of your idea, though, is not “find a magical codec that beats everything on everything,” but “build a codec that searches for short analytic descriptions when they exist, and falls back when they do not.” That framing is consistent with the explicit-formula picture, the Minimum Description Length principle, arithmetic coding, and the basic incompressibility barrier from algorithmic information theory. citeturn12view0turn21view1turn21view3turn25view0

## The screenshot is pointing at a real compression principle

What your screenshot is showing is not numerology. In the site’s Level 4 visualization, the gold curve is the weighted prime staircase \(\psi(x)\), and the cyan curve is \(x\) minus a sum of wave-like contributions, one per zeta zero. The page explicitly states that with zero zeros the reconstruction is just a ramp, with about thirty zeros it develops “knuckles,” and with about one hundred zeros it locks onto every visible step on the displayed interval \([2,100]\). In the underlying exact mathematics, \(\psi(x)\) is related to an infinite sum over the nontrivial zeros, plus correction terms; the visual “100 zeros rebuild the primes exactly” is therefore an interval-limited truncation phenomenon, not a claim that one hundred zeros globally encode all primes once and for all. citeturn12view0turn4search14

That matters because it already tells you the right abstraction for compression: **find the coordinate system in which the object is simple**. The site even says the zeros are “a complete description of the primes” and likens them to a spectrum or change of coordinates. In other words, the screenshot is not really about primes first. It is about representational economy. The primes look irregular in one basis and structured in another. Compression succeeds for exactly the same reason. citeturn12view0

It is also worth separating the explicit formula from the Riemann Hypothesis itself. The explicit formula linking primes and zeros is exact mathematics; RH is the additional claim that every nontrivial zero lies on the critical line \(\Re(s)=\tfrac12\), which would force the prime-counting error term to have essentially square-root scale. RH remains unproved, and rigorous computations have verified it for zeros up to height \(3\times 10^{12}\), but that still falls far short of a proof. citeturn13search3turn14search0

## What symbolic regression can and cannot buy you

The strongest theoretical foundation for your idea is not “symbolic regression” by itself. It is **MDL**. Grünwald’s MDL tutorial states the core principle very plainly: any regularity in data can be used to compress it, and better compression corresponds to having captured more of the data’s real structure. MDL also gives you the right tradeoff between fit and model complexity, which is exactly what a symbolic-regression compression project needs if you want it to stay mathematically disciplined instead of degenerating into overfitted formula-hunting. citeturn21view1

But MDL also forces intellectual honesty. Counting arguments in Kolmogorov complexity show that incompressible strings must exist, and in fact most long strings are close to incompressible. So there cannot be a single lossless compressor that strictly shrinks every possible file. “Universal” is possible only in a qualified sense: for example, Rissanen’s universal coding results concern asymptotic optimality over source classes such as stationary ergodic sources, not guaranteed wins on every concrete bitstring. citeturn25view0turn16search0

That means your project should not aim for “a universal compressor that beats everything.” It should aim for **a universal container format with a symbolic-model branch**. Every chunk is allowed to try a symbolic description, but every chunk also has a safe escape hatch into a conventional coder or raw storage. If the symbolic model helps, keep it. If not, fall back. That way the codec is universal in the practical engineering sense—able to encode arbitrary data—without violating the theoretical fact that many strings simply do not have shorter descriptions. citeturn25view0turn16search0turn21view1

Symbolic regression is a plausible search mechanism for the “discover a short description” step, but it is computationally hard. A 2022 TMLR paper proves that symbolic regression is NP-hard, and the paper’s review of the area emphasizes that practical systems either use heuristics or restrict the search space. That does not kill your idea. It just means your design has to be staged, budgeted, and basis-aware from day one. citeturn26view0

The hidden difficulty is coordinates. SINDy is extremely explicit about this: sparse equation discovery works only when the measurement variables and function basis are appropriate, and there is “no single method” that solves all coordinate-choice problems. AI Feynman succeeds precisely because many real scientific formulas have extra structure—symmetry, separability, compositionality—that can be exploited to prune search. The Riemann screenshot works because the right coordinates are already known: \(x\), \(\log x\), prime powers, and the zero ordinates \(\gamma\). If you run symbolic regression on raw bytes with no smart features, you should expect failure. If you give it the right transformed coordinates, the story changes dramatically. citeturn23view0turn27view0

## A mathematically grounded codec architecture

The cleanest design is an **MDL-guided symbolic residual codec**. For each segment of data, you minimize a true codelength objective of the form

\[
L_{\text{total}}
=
L(\text{segment type})
+
L(\text{model tree})
+
L(\text{constants})
+
L(\text{side information})
+
L(\text{data}\mid \text{model}).
\]

That is just MDL in compression clothing: the model is paid for explicitly, and then the remaining surprise is encoded conditionally on the model. Because arithmetic coding cleanly separates “the model” from “the encoding,” it is the natural backend for the conditional term. citeturn21view1turn21view3

There are two branches worth pursuing in parallel. The first is the direct **analytic-value branch**: the model predicts values from coordinates, residuals are computed exactly, and the residuals are entropy-coded. This is best for 1D and 2D coordinate-indexed data such as integer sequences, sensor logs, scientific arrays, grayscale image patches, procedural textures, and synthetic mathematics datasets—domains where compact formulas are actually plausible. The second is the **symbolic-predictor branch**: the model does not predict values directly, but probabilities of the next bit or byte from context features, and arithmetic coding turns those probabilities into compressed bits. That second route is much closer to how strong general-purpose compressors already work. citeturn21view3turn22view5turn22view6

This is where your “obscure hack” becomes genuinely interesting. PAQ-style compressors already combine multiple context models and feed the resulting probabilities into arithmetic coding. ZPAQ goes even further: its stream can contain instructions that specify model architecture and byte-code programs for computing contexts and transforms. So the idea of “ship the model with the compressed data” is not weird at all. Your twist would be to replace hand-designed or manually tuned contexts with contexts, formulas, or transforms discovered by symbolic regression and selected by MDL. citeturn22view5turn22view6turn21view3

The safest practical guarantee is simple: **the symbolic branch only wins when its full bit cost is smaller than the fallback branch**. That means including the model tree, constants, chunk headers, partition map, and residual code length in the comparison. If it loses, store the chunk with the fallback coder. This keeps the compressor honest and prevents beautiful formulas from making files bigger. It also turns the whole project into a clean scientific question: *for which data classes does symbolic-model search beat the fallback after paying the full representation cost?* That is exactly the right research question. citeturn21view1turn21view3

If you want one Riemann-inspired design principle to carry throughout the project, I would make it this: **search on transformed coordinates, not only on raw index**. For 1D data, give the system access to \(i\), \(i/N\), \(\log(i+c)\), cumulative sums, finite differences, and oscillatory primitives like \(\sin(\omega \log(i+c)+\phi)\) or \(\cos(\omega i+\phi)\). For 2D data, supply \(x\), \(y\), radial terms, low-order polynomials, and frequency atoms. SINDy’s analysis supports this emphasis on basis choice, and the Riemann picture is a dramatic case study in why the right coordinate system can make an apparently jagged object sparse. citeturn23view0turn12view0

## The best search stack for a Jupyter-first prototype

For a notebook-first research workflow, PySR is the most practical starting point. Its paper describes it as a practical symbolic-regression tool with a high-performance Julia backend, a multi-population evolutionary search, and an evolve-simplify-optimize loop built specifically to discover interpretable expressions and tune unknown constants efficiently. That makes it a very good “default engine” for the early notebooks. citeturn21view4

I would not rely on only one search engine, though. AI Feynman should be in the stack because it is very good when the target has symmetries, separability, or compositional decompositions, which many synthetic compression targets and physically generated sequences do. Exhaustive symbolic regression should also be in the stack for small expression classes and small chunks, because deterministic or near-exhaustive search is often more reliable than stochastic GP when the true formula is short. The ESR literature is explicit that stochastic symbolic regression can fail to find the best solution even when that solution is simple. citeturn27view0turn22view2

For dynamical data, SINDy is not optional—it is a separate mode. If your chunk is a sampled trajectory, a physical simulator output, or something that plausibly lives on a low-dimensional manifold with sparse governing dynamics, SINDy’s sparse-library approach can be far more sample-efficient than general expression evolution. Its own paper also gives the most important warning: success depends on giving it the right state variables and sparsifying basis. citeturn23view0

The most compression-aligned direction in current symbolic-regression research is MDLformer-guided search. The point of that work is precisely that prediction error is often the wrong search objective for recovering the right symbolic form, whereas description length is much closer to the target. Whether or not you eventually use that exact method, the principle is exactly right for your project: **do not optimize MSE first and hope compression follows; optimize code length directly**. citeturn22view3turn21view1

Because symbolic regression is NP-hard, the correct engineering posture is portfolio-based rather than ideological. Use PySR as the general evolutionary worker, AI Feynman when simplifications are plausible, SINDy on dynamical segments, and exhaustive search on tiny grammars. Then let MDL decide which discovered model, if any, is worth transmitting. That is much closer to a serious compression research program than betting on one monolithic GP engine. citeturn26view0turn21view4turn27view0turn22view2turn23view0

## How to design the fitness function and benchmarks

The fitness function should be **bits**, not regression error. In practice, that means you should measure for every candidate:

\[
\text{fitness}
=
L(\text{AST})
+
L(\text{constants})
+
L(\text{partition})
+
L(\text{residual stream or arithmetic-coded data}).
\]

Any surrogate objective that ignores one of those terms will push the search toward pretty but useless formulas. This is exactly the failure mode MDL was designed to avoid, and it is also why code-length-aware search is a better fit than pure numeric approximation. citeturn21view1turn22view3

Your benchmark ladder should have three tiers. First, use **synthetic and semi-synthetic structured data**: formula-generated integer sequences, oscillatory staircases, low-order PDE snapshots, procedural images, and “Riemann-inspired” wave-plus-step datasets. This is where the symbolic branch has a genuine chance to shine and where you can learn whether the modeling pipeline is working. Second, use **structured real-valued datasets** such as scientific time series or gridded arrays. Third, use **heterogeneous byte corpora** such as Canterbury and Silesia, and text benchmarks such as enwik8/enwik9, to test whether the symbolic branch ever helps once you leave friendly domains. Canterbury exists precisely as a benchmark for lossless compression methods; Silesia is widely used for larger heterogeneous files; Mahoney’s enwik9 benchmark is explicitly about modeling quality and even counts decompressor size in its ranking. citeturn22view7turn22view8turn22view9

One subtle but very important benchmarking point: if you ever want to make serious public claims, report both **research compression ratio** and **challenge-style total size**. Mahoney’s large text benchmark counts the size of the decompressor as well as the compressed data. Early Jupyter work does not need to do that, but the moment you compare yourself to real compressors, you need a clean story about decoder cost, memory use, and determinism. citeturn22view9

Because most strong symbolic-regression methods are stochastic, every reported point should come from repeated runs under fixed budgets. The ESR literature explicitly notes that stochastic methods have unknown failure probabilities; that is a direct warning that single-seed “hero runs” are not scientifically convincing. Fix evaluation budget, wall-clock budget, and memory budget, and then report median, variance, and best-found code length across seeds. citeturn22view2

The ablations should be ruthless. Turn off transformed coordinates. Turn off oscillatory primitives. Turn off piecewise segmentation. Turn off constant refinement. Turn off fallback. Turn off MDL and replace it with MSE. If a component matters, you should be able to see its contribution in compressed bits, not only in fit plots. That kind of ablation discipline is what will stop the project from becoming an aesthetic exercise. citeturn21view1turn23view0

## The first notebook roadmap I would actually build

I would build this project in a very specific order, and I would resist the temptation to start with arbitrary files.

1. **Build a Riemann sanity notebook first.** Reproduce the \(\psi(x)\) reconstruction idea from the site, then encode “trend + selected oscillatory terms + residual” as if it were a codec. The purpose of this notebook is not to beat existing compressors; it is to make the MDL accounting concrete and to train your intuition on how a jagged staircase can become sparse in the right basis. citeturn12view0turn4search14

2. **Build a lossless 1D symbolic residual codec next.** Use chunked integer sequences indexed by position, transformed position, cumulative sums, and a small oscillatory library. Search with PySR, refine constants, round deterministically, compute exact residuals, and arithmetic-code those residuals. This is the smallest setting in which your core idea can either work or fail cleanly. citeturn21view4turn21view3

3. **Only after that, add the symbolic-predictor branch.** Here the model outputs next-bit or next-byte probabilities from a modest context feature set, and an arithmetic coder handles exact coding. Conceptually this is much closer to PAQ/ZPAQ, but now the context transformations or mixers are being searched rather than hand-built. If this branch works at all, it is your best route toward genuinely broad utility. citeturn22view5turn22view6turn21view3

4. **Then run a benchmark notebook with real discipline.** Use synthetic structured sets, then Canterbury, then Silesia, then enwik8/enwik9-like text settings. Fix budgets, repeat seeds, include fallback comparisons, and track compressed bits, encode time, decode time, peak memory, and decoder assumptions. If the symbolic branch wins only on narrow domains, that is still a valid research outcome. citeturn22view7turn22view8turn22view9turn22view2

My bottom-line recommendation is this: frame the whole project as **MDL-guided coordinate discovery with exact residual coding**. The Riemann screenshot is a beautiful proof-of-concept for the meta-idea that the right basis can make a jagged discrete structure sparse. Symbolic regression is then not the codec by itself; it is the search mechanism for discovering that basis or predictor when one exists. If you hold onto that distinction, the project becomes both mathematically defensible and genuinely original. citeturn12view0turn21view1turn21view3turn26view0