# 🐱 KittyLM

### Independent Language Model Research & Development

**From first principles to intelligent systems.**

![Status](https://img.shields.io/badge/Status-Active%20Research-8B5CF6)
![Version](https://img.shields.io/badge/Version-0.1.0--dev-blueviolet)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![License](https://img.shields.io/badge/Code%20License-Apache--2.0-blue)

---

## 💜 Welcome to KittyLM

**KittyLM** is an independent language model research and engineering project created by [KrazyKitty](https://github.com/krazykitty2503).

The project focuses on understanding, designing, implementing, training and evaluating language models from first principles, with an emphasis on **reproducibility, architectural experimentation, computational efficiency, security and scientific evaluation**.

Rather than beginning with a large pretrained model, KittyLM starts with a small, purpose-built autoregressive Transformer. Every major component, from tokenisation and neural architecture to checkpointing, inference and evaluation, is developed and tested as part of a controlled engineering workflow.

The ambition extends beyond one language model.

KittyLM is intended to become the foundation of an evolving family of models, supporting future research into efficient neural architectures, advanced reasoning, persistent memory, specialist capabilities and increasingly sophisticated AI systems.

> **Our philosophy:** Build it. Measure it. Understand it. Improve it.
>
> **Our mission:** Engineer original language models through experimentation, measurable progress and a deep understanding of the systems that make modern AI possible.

### Project at a glance

| Property | Description |
|---|---|
| Project | KittyLM |
| Developer / Owner | KrazyKitty |
| Current package version | `0.1.0.dev0` |
| Project category | Artificial Intelligence / Machine Learning Research |
| Primary language | Python |
| ML framework | PyTorch |
| Model family | Decoder-only autoregressive Transformers |
| Primary focus | From-scratch language model engineering |
| Target acceleration | AMD GPUs / ROCm |
| Development stage | Experimental / Pre-release |
| Future direction | A family of research and specialist language models |

**Important:** KittyLM 0.1 is a research platform, not a production-ready general-purpose AI assistant. No formally pretrained model weights or general-purpose model capabilities are being advertised.

---

## 01 // Research Objectives

KittyLM is being developed around six primary objectives.

**01. Original Model Engineering**

Design and implement core language model components independently, enabling direct investigation of their behaviour, limitations and performance.

**02. Scientific Reproducibility**

Develop deterministic experiments, versioned datasets, verified checkpoints and structured evaluation records.

**03. Efficient AI Development**

Study GPU utilisation, attention implementations, mixed precision, memory consumption, inference performance and training efficiency.

**04. Architectural Innovation**

Establish reliable baseline measurements before exploring alternative sequence mixers, hybrid architectures, expert models and other experimental techniques.

**05. Security & Reliability**

Apply secure development practices to model checkpoints, datasets, generated output, dependencies, CI/CD pipelines and research artifacts.

**06. Long-Term Model Evolution**

Build the engineering foundation for increasingly capable KittyLM generations without sacrificing maintainability, transparency or scientific validity.

---

## 02 // System Architecture

KittyLM follows a modular architecture designed to separate model development, tokenisation, datasets, training, inference, evaluation and experimental reporting.

### Research pipeline

```text
                  KITTYLM RESEARCH SYSTEM
                           |
              +------------+------------+
              |                         |
          TOKENISER                  DATASETS
          Byte BPE                   Provenance
          Special tokens             Licensing
          Vocabulary                 Filtering
              |                         |
              +------------+------------+
                           |
                      MODEL CORE
                           |
                 Decoder-only Transformer
                 RMSNorm / RoPE / SwiGLU
                 Causal Attention / KV Cache
                           |
                      TRAINING
                           |
                  AdamW Optimisation
                  Learning Rate Schedule
                  Mixed Precision
                  Checkpoint / Resume
                           |
                      EVALUATION
                           |
                  Cross-Entropy Loss
                  Perplexity / BPB
                  Generation Accuracy
                  Inference Throughput
                           |
                   EXPERIMENT LEDGER
                           |
                  Verified Run Records
                  Reproducible Results
                  Comparative Analysis
                           |
                    FUTURE RESEARCH
                           |
                 Advanced Architectures
                 Optimised Inference
                 Specialist Models
                 Integration Systems
```

The diagram includes both implemented components and intended future development boundaries. Consult [the architecture documentation](docs/architecture.md) for their individual implementation statuses.

### Transformer baseline

KittyLM's primary research baseline uses a compact LLaMA-inspired decoder-only Transformer.

Its architectural features include:

- Causal autoregressive language modelling
- Pre-normalisation residual Transformer blocks
- Root Mean Square Layer Normalisation (RMSNorm)
- Rotary Position Embeddings (RoPE)
- Multi-head causal self-attention
- SwiGLU feed-forward networks
- Tied input embedding and output projection weights
- Key-value caching for autoregressive inference
- Explicit parameter accounting
- Configurable attention backends
- Deterministic configuration and test infrastructure

The architecture also provides a sequence-mixer extension point for future experiments with alternative neural components.

These extensions are not assumed to be implemented or validated merely because the interface exists.

---

## 03 // Model Configurations

The repository includes two principal configurations.

| Specification | Nano | Tiny |
|---|---:|---:|
| Hidden dimension | 128 | 384 |
| Transformer layers | 4 | 6 |
| Attention heads | 4 | 6 |
| Feed-forward dimension | 384 | 1,024 |
| Context length | 256 | 1,024 |
| Configured vocabulary | 16,384 | 16,384 |
| Architecture | Decoder-only | Decoder-only |
| Intended role | Engineering validation | Research baseline |

The Tiny baseline contains **16,913,280 parameters** in its documented 16,384-vocabulary configuration.

Nano supports a smaller, 512-token smoke vocabulary override for targeted engineering tests.

These configurations serve different research purposes.

**Nano** is designed to establish that model execution, gradient updates, checkpoint recovery and overfitting tests behave correctly.

**Tiny** is the intended reference model for controlled baseline training and subsequent architectural comparisons.

The objective is not to maximise parameter count prematurely. It is to establish a trustworthy baseline that can support meaningful research.

---

## 04 // Current Development Status

**Status snapshot: 10 October 2026**

The following table distinguishes merged repository milestones from pending or unverified work.

| Milestone | Engineering scope | Status |
|---|---|---|
| Foundation | Repository structure, configurations, security tooling, CI and documentation | ✅ Merged |
| A | Byte-level BPE tokenizer and validation | ✅ Merged |
| B | Transformer architecture, KV cache and attention benchmarks | ✅ Merged |
| C | Training engine, checkpoints and deterministic recovery | ✅ Merged |
| D | Evaluation, generation, inference speed and regression corrections | ✅ Merged |
| E | `SMOKE-GPU-001` GPU correctness and Nano overfit validation | 🔬 Verification pending |
| F | Curated `local-v1` dataset pipeline | Planned |
| G | Formal baseline experiments and tokenizer vocabulary ablations | Planned |

Milestone D was merged in commit [`d4c7e7d`](https://github.com/krazykitty2503/kittylm/commit/d4c7e7d9ac44558c8ab7d9960bf4bdb852bce242).

Subsequent GitHub dependency-maintenance changes are not equivalent to new ML milestones.

Milestone E work has been reported in a separate development workspace, but its final acceptance and merge have not been established from the current default branch.

### Engineering functionality implemented

The repository contains implementations and test coverage for:

- Deterministic byte-level BPE tokenisation
- Decoder-only Transformer inference
- Configurable attention and KV caching
- Model parameter accounting
- Optimisation and learning-rate scheduling
- Gradient accumulation and clipping
- Training checkpoint creation and recovery
- Deterministic resume testing
- Cross-entropy, perplexity and bits-per-byte evaluation
- Deterministic evaluation windowing
- Greedy and temperature-based text generation
- Top-k and top-p sampling
- Inference throughput measurement
- Secret scanning and artifact protection
- Structured experiment records
- Local checks and GitHub Actions CI

These are software engineering capabilities. Their existence does not establish that a generally useful pretrained model has been produced.

### Research evidence

The project has already documented targeted engineering measurements and checks, including CPU/GPU validation, checkpoint-resume comparisons and attention backend benchmarking.

On the previously tested AMD Radeon RX 9060 XT / ROCm environment, the attention benchmark selected the reference attention backend for the configured baseline.

Results are hardware- and environment-dependent.

Engineering smoke measurements must not be presented as formal language-model quality benchmarks.

For the evidence and limitations, consult:

- [Architecture](docs/architecture.md)
- [Decisions](docs/decisions.md)
- [Limitations](docs/limitations.md)
- [Experiment records](experiments/)
- [Discrepancy log](docs/discrepancies.md)

---

## 05 // Technical Stack

| Area | Technology |
|---|---|
| Language | Python 3.12+ |
| ML framework | PyTorch |
| Numerical computing | NumPy |
| Configuration | YAML / PyYAML |
| Tokenisation | Custom byte-level BPE |
| Hardware acceleration | ROCm-compatible PyTorch environment |
| Unit and integration testing | pytest |
| Linting and formatting checks | Ruff |
| Static typing | mypy |
| Dependency security | pip-audit |
| CI/CD | GitHub Actions |
| Version control | Git / GitHub |
| Research tracking | Experiment ledger and validated records |

KittyLM is developed primarily on a Windows workstation with an AMD GPU.

CPU-compatible workflows are maintained for automated CI, while GPU-specific tests are executed on authorised local hardware.

---

## 06 // Installation & Development

### Requirements

- Python 3.12 or later
- Git
- A compatible PyTorch installation
- Sufficient system memory for the selected model configuration
- A supported GPU environment for hardware-accelerated tests

**Maintenance advisory — 10 October 2026:** The current `main` branch has malformed development dependency entries in `pyproject.toml` following dependency-update merges. Installation from the latest `main` commit may fail until the dependency configuration is repaired and the required checks are rerun.

The following commands describe the intended Windows development workflow after that issue is resolved.

### Clone the repository

```bash
git clone https://github.com/krazykitty2503/kittylm.git
cd kittylm
```

Repository access currently requires appropriate GitHub permissions.

### Create the Python environment

For the existing Windows workstation with its separately managed PyTorch installation:

```powershell
py -3.12 -m venv --system-site-packages .venv
```

This environment inherits system-site packages. Ensure the inherited PyTorch build is compatible with the target device.

### Install development dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

### Configure local repository hooks

```bash
git config core.hooksPath .githooks
```

### Run the full local checks

```powershell
.\.venv\Scripts\python.exe scripts/check.py all
```

The project defines quality, test and security checks that should be completed before accepting milestone changes.

### GPU-specific tests

```powershell
.\.venv\Scripts\python.exe -m pytest -m gpu
```

GPU tests require a functioning GPU-enabled PyTorch environment and are not part of the ordinary hosted CPU CI workflow.

### Smoke tokenizer

```powershell
.\.venv\Scripts\python.exe scripts/train_tokenizer.py --config configs/tokenizer/smoke.yaml
```

Generated research artifacts belong in the designated run directories and must not be committed accidentally.

The repository includes additional scripts for evaluation, generation, benchmarking and CI evidence verification.

Always consult the script's supported arguments and current configuration before launching experiments.

---

## 07 // Repository Structure

```text
KittyLM/
|
+-- kittylm/
|   +-- tokenizer/       # BPE tokenisation
|   +-- model/           # Transformer architecture
|   +-- training/        # Optimisation and checkpoints
|   +-- evaluation/      # Model evaluation and metrics
|   +-- inference/       # Autoregressive generation
|   +-- data/            # Data utilities and loaders
|   +-- utils/           # Shared engineering utilities
|   +-- export/          # Future export boundary
|   +-- integration/     # Future integration boundary
|
+-- configs/             # Model and tokenizer configs
+-- scripts/             # Development and CLI tools
+-- tests/               # Automated verification
+-- experiments/         # Research and benchmark records
+-- docs/                # Architecture and governance
+-- .github/             # GitHub Actions and templates
+-- .githooks/           # Local Git security hooks
|
+-- pyproject.toml
+-- CONTRIBUTING.md
+-- SECURITY.md
+-- CODE_OF_CONDUCT.md
+-- DATA_SOURCES.md
+-- LICENSE
+-- README.md
```

The structure intentionally separates scientific experiments from reusable production-quality engineering components.

---

## 08 // Research Roadmap

KittyLM development follows a staged approach.

The future model generations below represent **research directions**, not claims of implemented functionality or committed release dates.

### KittyLM 0.1 — Foundation and Validation

Establish an understandable language model stack with strict testing, deterministic configurations, checkpoint safety, GPU validation and formal baseline experiments.

Primary objective: **Prove the model and research infrastructure work correctly.**

### KittyLM 0.2 — Dataset and Training Improvements

Potential research areas:

- Broader licensed technical corpora
- Improved deduplication
- More comprehensive evaluation
- Dataset mixture investigations
- Expanded tokenisation studies
- Better training throughput
- Improved checkpoint and experiment tooling

Primary objective: **Improve data quality, evaluation breadth and training reliability.**

### KittyLM 1.0 — Foundational Research Model

An intended milestone for establishing a more complete and reproducible trained baseline, subject to demonstrated training and evaluation results.

Potential priorities include stronger language modelling performance, release-ready model documentation, reproducible training recipes and usable inference interfaces.

### KittyLM 2.0 — Efficient and Hybrid Architectures

Proposed research topics:

- Gated Delta Networks and alternative sequence mixers
- Hybrid attention/recurrent architectures
- Mixture-of-Experts
- Training and inference optimisations
- Improved context handling
- Quantisation and efficient deployment

Each proposal must be evaluated against a controlled baseline.

### KittyLM 3.0 — Reasoning and Memory Research

Potential directions:

- Structured reasoning evaluation
- Retrieval-augmented generation
- External and persistent memory systems
- Adaptive computation
- Specialist coding and technical capabilities
- Reliable tool-use evaluation

### KittyLM 4.0+ — Advanced Model Systems

Long-term research possibilities include:

- Multimodal architectures
- More efficient scaling
- Distributed training
- Advanced model composition
- Specialised expert models
- Secure integrations with broader agent and computing systems

These features will only become implementation commitments through future specifications, experiments and approved development milestones.

**No future version number implies an unverified capability or guaranteed release.**

---

## 09 // Scientific Methodology

KittyLM research is evidence-driven.

Experiments should define their objectives and controls before execution, rather than selecting favourable metrics after results are obtained.

### Experimental standards

Each formal experiment is expected to record:

- Experiment identifier and purpose
- Source commit and CI evidence
- Model and tokenizer configurations
- Dataset version and provenance
- Random seeds
- Hardware and software environment
- Optimiser and training settings
- Resource and timing measurements
- Evaluation metrics and limitations
- Checkpoint and reproducibility evidence

### Core evaluation metrics

| Metric | Purpose |
|---|---|
| Cross-entropy loss | Next-token prediction performance |
| Perplexity | Exponentiated mean token loss |
| Bits-per-byte | Comparison across tokenizer vocabularies |
| Gradient norms | Training stability diagnostics |
| Token-match accuracy | Targeted overfit validation |
| Tokens per second | Inference/training throughput |
| GPU memory usage | Hardware efficiency |
| Resume equivalence | Recovery and reproducibility |

Formal research findings require validated records and appropriate experimental controls.

Engineering smoke tests can demonstrate that the stack functions, but cannot establish broad model quality.

---

## 10 // Security, Safety & Responsible Research

Security is a fundamental part of KittyLM's engineering approach.

The project includes controls intended to reduce accidental leakage, artifact corruption, unsafe checkpoint loading and unreproducible experimentation.

### Security principles

- Do not commit credentials, secrets or private training data.
- Preserve data provenance and licence information.
- Scan incoming corpus material for sensitive content.
- Use controlled checkpoint loading and integrity validation.
- Keep generated research artifacts separate from source code.
- Maintain dependency and CI security checks.
- Require authorization before external uploads or model publication.
- Treat datasets and retrieved materials as untrusted inputs.
- Prevent automatic online learning from unreviewed feedback.

### Responsible use

KittyLM is experimental software.

Generated material may be inaccurate, insecure, misleading or unsuitable for real-world decisions.

Its small-scale training and evaluation infrastructure must not be mistaken for evidence of general intelligence, reliable cybersecurity expertise or production readiness.

Further information:

- [Security Policy](SECURITY.md)
- [Responsible Use](docs/responsible-use.md)
- [Safety Documentation](docs/safety.md)
- [Known Limitations](docs/limitations.md)

---

## 11 // Development Philosophy

KittyLM is built around a few essential engineering principles.

**Correctness before complexity.**

A working baseline is more valuable than an advanced architecture that cannot be properly evaluated.

**Evidence before claims.**

Every significant technical conclusion should be backed by reproducible measurements, tests or documented observations.

**Security by design.**

Datasets, checkpoints, development infrastructure and model outputs should be handled with appropriate protections from the beginning.

**Research before optimisation.**

Performance improvements must be measured against established reference implementations.

**Human-directed development.**

AI tools assist with implementation, review and research, while final engineering and release decisions remain under human project ownership.

**Learning through engineering.**

The objective is not simply to use existing AI technology, but to understand how it works by building and measuring it.

---

## 12 // Collaboration & Contributions

KittyLM is created and led by **KrazyKitty**.

Development is supported by AI-assisted engineering, including Claude for implementation assistance and ChatGPT for architectural discussion and independent technical review.

All accepted changes remain subject to the project's engineering, security and research standards.

Contributions, issues and architectural suggestions should follow:

- [Contribution Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Architecture Decisions](docs/decisions.md)
- [Open Development Backlog](docs/backlog.md)

Significant architecture or research-scope changes should be proposed and reviewed before implementation.

### Project links

**Developer:** [KrazyKitty](https://github.com/krazykitty2503)

**Project repository:** [krazykitty2503/kittylm](https://github.com/krazykitty2503/kittylm)

**Website:** [krazykitty.dev](https://krazykitty.dev)

**Research profile:** [KrazyKitty on Hugging Face](https://huggingface.co/KrazyKitty)

---

## 13 // Licensing

KittyLM separates code, documentation, model weights and training-data licensing.

| Component | Licence |
|---|---|
| Source code | [Apache License 2.0](LICENSE) |
| Model weights, if released under the current policy | [MODEL_LICENSE.md](MODEL_LICENSE.md) |
| Documentation | [CC BY 4.0](docs/LICENSE.md) |
| Training datasets | Individual source licences |
| Third-party dependencies | Their respective licences |

The presence of a model-weight licence does not imply that trained weights have been released.

Dataset usage and redistribution must comply with each source's applicable terms.

See [DATA_SOURCES.md](DATA_SOURCES.md) for the dataset provenance register.

---

## 💜 The Vision Behind KittyLM

KittyLM began with a simple question:

**What if I built my own language model, from the foundations upwards, and learned to understand every part of it?**

That question became an engineering and research project.

One that combines programming, mathematics, machine learning, systems engineering, GPU computing, cybersecurity and a determination to keep learning.

KittyLM is not about claiming to have built the largest or most intelligent model.

It is about building something original, understanding its design, measuring its behaviour, learning from every failure and improving it one milestone at a time.

Every tokenizer, model component, experiment and engineering decision contributes to a deeper understanding of artificial intelligence.

And this is only the beginning.

### `KITTYLM // BUILD. MEASURE. LEARN. EVOLVE.`

*Engineered with curiosity, powered by research, and created with 💜 by KrazyKitty.*

---

**Copyright © 2026 KrazyKitty.**

*KittyLM is an independent language model research project. All future capabilities and releases remain subject to technical validation, applicable licensing and project approval.*
