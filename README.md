# MarketPrism — Sortition Evaluation Simulations

Monte Carlo simulations for evaluating committee-selection (sortition) protocols under varying rates of honest, lazy, and adversarial participants. Two variants are included:

| Directory | Executable | Protocol |
|-----------|------------|----------|
| `regular/` | `monte_carlo` | Uniform random sortition |
| `weighted/` | `weighted_monte_carlo` | Weighted sortition across two sub-populations |

---

## Prerequisites

- CMake ≥ 3.29
- A C++20-capable compiler (clang++ or g++)
- [xtensor](https://xtensor.readthedocs.io/en/latest/installation.html)

### Installing xtensor (macOS)

```bash
brew install xtensor
```

### Installing xtensor (Ubuntu/Debian)

```bash
sudo apt install libxtensor-dev
# or via conda:
conda install -c conda-forge xtensor
```

---

## Build

Each program is built independently from its own directory.

### regular/monte\_carlo

```bash
cd regular
cmake -B build -S .
cmake --build build
```

The executable is at `regular/build/monte_carlo`.

### weighted/weighted\_monte\_carlo

```bash
cd weighted
cmake -B build -S .
cmake --build build
```

The executable is at `weighted/build/weighted_monte_carlo`.

---

## Run

### monte\_carlo

```
./build/monte_carlo <lazy_rate> <adversarial_rate> <committee_size>
```

| Argument | Type | Description |
|----------|------|-------------|
| `lazy_rate` | float [0,1] | Fraction of the population that is lazy |
| `adversarial_rate` | float [0,1] | Fraction of the population that is adversarial |
| `committee_size` | int | Number of members per committee |

The simulation draws 10 threads × 1 000 trials each. Results (the round at which a committee succeeded, or `fail`) are written to a file named:

```
<committee_size>_lazy_<lazy_rate>_adv_<adversarial_rate>.txt
```

**Example**

```bash
cd regular
./build/monte_carlo 0.10 0.20 100
# output: 100_lazy_0.10_adv_0.20.txt
```

---

### weighted\_monte\_carlo

```
./build/weighted_monte_carlo <lazy_rate> <adversarial_rate> <committee_size> <adv_rate_in_A> <rate_bucket_A>
```

| Argument | Type | Description |
|----------|------|-------------|
| `lazy_rate` | float [0,1] | Fraction of the population that is lazy  |
| `adversarial_rate` | float [0,1] | Overall adversarial rate across both buckets |
| `committee_size` | int | Total committee size |
| `adv_rate_in_A` | float [0,1] | Proportion of adversaries concentrated in bucket A |
| `rate_bucket_A` | float [0,1] | Fraction of committee seats drawn from bucket A (B gets `1 - rate_bucket_A`) |

Results are written to:

```
<rate_bucket_A>/weighted_<adv_rate_in_A>:<committee_size>_lazy_<lazy_rate>_adv_<adversarial_rate>.txt
```

**Example**

```bash
cd weighted
./build/weighted_monte_carlo 0.10 0.20 100 0.70 0.60
# output: 0.60/weighted_0.70:100_lazy_0.10_adv_0.20.txt
```

---

## Output format

Each line of the output file is either:

- An integer — the committee index (1-based) at which a valid committee was found in that trial.
- `fail` — no valid committee was found in that trial.