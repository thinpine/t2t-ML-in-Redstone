**Our Minecraft Redstone text-to-text simulation relies on a Multinomial Naive Bayes (NB) classifier rather than a complex transformer.** We chose NB because its inference mathematics reduce entirely to counting and addition of log-probabilities, avoiding matrix multiplications and floating-point comparisons that are intractable in vanilla Redstone.

**To optimize for hardware constraints, we iterated through several key Machine Learning, Software, and Hardware configurations:**

### 1. Tokenization & Feature Engineering:
We initially tested a character bigram model mapping to 32 slots, but it yielded poor precision (~40%). We shifted to a word-level approach, but storing a traditional vocabulary lookup table would require massive, impractical amounts of ROM. We resolved this by engineering an 8-bit Shift-XOR Hashing Tokenizer. This algorithm mathematically hashes variable-length words on-the-fly into 256 physical hardware slots (0-255) without a dictionary. Three additional bypass slots (256-258) were hardwired for structural metadata (?, !, and >8 word lengths), resulting in a highly efficient 259-feature space.

### 2. Quantization: 
We evaluated 4-bit and 8-bit uniform quantization for the network's weights. While 4-bit perfectly matches Redstone's native 16 signal strength levels, a distributional audit revealed that our model's weights cluster tightly between -2 and -16. 4-bit quantization crushed this critical sub-interval into just a few discrete bins, causing rounding collisions and severe accuracy degradation. We finalized on 8-bit quantization, storing values across two stacked 4-bit barrels, to preserve the classifier's decision boundaries.

### 3. ALU & Accumulator Width: 
With 259 active features outputting 8-bit signed weights, worst-case density calculations showed the accumulated negative score could reach -32,893. Because a standard 16-bit signed integer underflows at -32,768, we expanded the hardware logic to use 17-bit Ripple-Carry Adders and 17-bit accumulators to safely process massive inputs without integer wrap-around.