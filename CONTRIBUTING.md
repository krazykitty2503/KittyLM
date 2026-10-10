# Contributing to KittyLM

**Scientific Integrity · Reproducible Research · Engineering Excellence · Responsible AI Development**

**Project:** KittyLM — Independent Language Model Research & Development  
**Project Owner & Lead Architect:** KrazyKitty  
**Policy Version:** 1.0  
**Last Updated:** 10 October 2026  
**Repository:** [krazykitty2503/kittylm](https://github.com/krazykitty2503/kittylm)

---

## 01 // Introduction

Thank you for your interest in contributing to **KittyLM**.

KittyLM is an independent artificial intelligence and machine learning research project focused on understanding, implementing, training, evaluating and improving language models from first principles.

The project emphasises scientific reproducibility, secure software engineering, transparent experimentation, data provenance and responsible AI development.

KittyLM is currently a small, single-maintainer research project, with development supported by AI-assisted engineering and independent technical review.

Contributions may include software improvements, research proposals, documentation, testing, security improvements, benchmark methodology, architectural analysis and experimental findings.

All contributions must align with the project's approved research objectives, engineering standards and development governance.

**Our philosophy:**

> Build it. Measure it. Understand it. Improve it.

**Our core engineering principles:**

1. Correctness before complexity.
2. Evidence before technical claims.
3. Reproducibility before benchmark publication.
4. Security and provenance by design.
5. Maintainability before premature optimisation.
6. Human oversight of significant project decisions.
7. Transparent reporting of successes, failures and limitations.

### Fundamental Research Rule

**No formal research result may be accepted without a validated experiment record and appropriate supporting evidence.**

Formal results are recorded under:

`experiments/<ID>/record.yaml`

The summary table:

`experiments/ablations.md`

is generated from validated records and must never be modified manually.

Engineering measurements and smoke-test diagnostics must be clearly distinguished from formal research findings.

---

## 02 // Community Standards

All contributors must follow the [KittyLM Code of Conduct](CODE_OF_CONDUCT.md).

KittyLM encourages respectful scientific discussion, constructive criticism, collaboration and independent thinking.

Technical disagreements should be addressed through evidence, documentation and reproducible testing.

Contributors are expected to:

- Respect differing technical perspectives.
- Provide specific and constructive feedback.
- Credit original authors and researchers.
- Acknowledge mistakes and correct them.
- Avoid personal attacks, harassment or intimidation.
- Disclose relevant research limitations.
- Respect project governance and contributor boundaries.
- Treat honest experimental failures as opportunities for learning.

A contributor's qualifications, experience or reputation do not replace technical evidence.

**Research ideas may be challenged rigorously. Contributors must be treated respectfully.**

---

## 03 // Project Governance & Development Authority

### 3.1 Project Ownership

KittyLM is created and maintained by **KrazyKitty**, who retains final authority over:

- Architectural direction
- Milestone planning and acceptance
- Repository administration
- Dataset approval and expansion
- Dependency and framework changes
- Model training and research experiments
- Hardware and infrastructure allocation
- Security policy
- Model publication and releases
- External integrations and collaborations

Contributors may propose changes, but submitting a proposal does not authorise its implementation.

### 3.2 Approved Implementation Plan

The approved implementation plan, currently **revision 3.3 unless formally superseded**, governs the project's implementation sequence.

The milestone ordering is defined by decision D-015.

The planned sequence is:

```text
Foundation
    |
    v
Milestone A — Tokeniser
    |
    v
Milestone B — Model Architecture
    |
    v
Milestone C — Training Engine
    |
    v
Milestone D — Evaluation & Generation
    |
    v
Milestone E — GPU Smoke Validation
    |
    v
Milestone F — Dataset Pipeline
    |
    v
Milestone G — Formal Experiments
```

Previously completed milestones are not to be repeated or reconstructed without an approved reason.

The current milestone status must be established from the repository, accepted milestone reports and relevant CI evidence.

Do not assume the state recorded in historical documentation is still current.

### 3.3 Changes Outside the Approved Plan

The following activities require explicit project approval:

- Introducing a new neural architecture
- Modifying an approved model architecture
- Expanding the dataset or adding external sources
- Introducing new major dependencies or frameworks
- Launching training or evaluation experiments outside the approved scope
- Changing required CI policies
- Altering experiment acceptance criteria
- Changing checkpoint or tokenizer compatibility contracts
- Publishing model weights or research artifacts
- Modifying project infrastructure or repository permissions

When implementation reveals a conflict with the accepted plan:

1. Stop the affected operation.
2. Record the discrepancy.
3. Identify the conflicting decision or assumption.
4. Explain the technical impact.
5. Propose a corrective change.
6. Obtain approval for any necessary plan revision.
7. Continue only after the relevant approval.

Discrepancies are tracked in [docs/discrepancies.md](docs/discrepancies.md).

Decisions are recorded in [docs/decisions.md](docs/decisions.md).

---

## 04 // Types of Contributions

KittyLM welcomes proposals in the following areas.

### 4.1 Software Engineering

- Bug fixes and regression tests
- Improved error handling
- Static typing and code quality
- Performance profiling
- Security improvements
- Documentation improvements
- Configuration validation
- Checkpoint and recovery reliability
- Build and development tooling

### 4.2 Machine Learning Research

- Transformer architecture analysis
- Tokenisation research
- Attention mechanism evaluation
- Optimisation and training studies
- Numerical precision investigations
- Model evaluation methodology
- Reproducibility improvements
- Controlled architectural ablations
- Inference efficiency research

### 4.3 Data Engineering

- Dataset provenance improvements
- Licence and permission verification
- Filtering and deduplication methodology
- Dataset quality validation
- Training and validation separation
- Data leakage detection
- Dataset versioning and reproducibility

Dataset additions require specific approval.

### 4.4 Security Research

- Secure checkpoint handling
- Secret detection
- Dependency vulnerability analysis
- Dataset ingestion security
- Supply-chain hardening
- CI/CD security improvements
- Safe model artifact handling

Potential vulnerabilities must follow [SECURITY.md](SECURITY.md).

### 4.5 Documentation & Scientific Communication

- Architecture explanations
- Research methodology
- Experimental limitations
- Developer documentation
- Reproducibility instructions
- Benchmark interpretation
- Design decision records
- Responsible-use guidance

Documentation contributions are subject to the same accuracy standards as code contributions.

---

## 05 // Development Environment

### 5.1 Prerequisites

KittyLM development currently targets:

- Python 3.12+
- PyTorch
- NumPy
- PyYAML
- pytest
- Ruff
- mypy
- Git
- GitHub Actions

GPU development uses a supported local AMD/ROCm PyTorch environment.

The exact software and driver versions must be recorded for experiments.

Refer to the [README](README.md) for the current setup instructions.

### 5.2 Clone the Repository

```bash
git clone https://github.com/krazykitty2503/kittylm.git
cd kittylm
```

Repository access requires appropriate permissions when the project is private.

### 5.3 Create a Python Environment

The existing Windows development configuration uses:

```powershell
py -3.12 -m venv --system-site-packages .venv
```

The `--system-site-packages` option permits the environment to inherit the locally installed PyTorch build.

Contributors should verify compatibility with their own environment rather than assume the same GPU or driver configuration applies.

### 5.4 Install Development Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Before installation, confirm that `pyproject.toml` is valid and that the selected dependency versions are consistent.

Dependency updates must be reviewed and tested.

### 5.5 Configure Git Hooks

```bash
git config core.hooksPath .githooks
```

The repository's pre-commit hook checks staged changes for secrets and forbidden artifacts.

Do not bypass these protections simply to complete a commit.

---

## 06 // Coding Standards

### 6.1 Python Engineering Requirements

Contributions should follow these conventions:

- Python 3.12-compatible code.
- Type annotations where practical.
- Readable, maintainable implementations.
- Small, testable functions and components.
- Clear public interfaces.
- Consistent error handling.
- Appropriate input validation.
- Standard-library logging.
- Explicit configuration rather than hidden behaviour.
- Deterministic behaviour where required.
- No unnecessary dependencies or frameworks.

The project uses Ruff and mypy for static quality checks.

Contributors should run the configured tools rather than substitute unrelated formatters or type-checking policies.

### 6.2 Module Boundaries

KittyLM separates core engineering concerns through Python subpackages.

Existing architectural constraints include:

- `kittylm.model` must not import `kittylm.training`.
- `kittylm.model` must not import `kittylm.data`.
- `kittylm.tokenizer` must not import PyTorch.
- Model architecture must remain separable from training orchestration.
- Evaluation must not depend on training implementation internals.
- Research tooling must respect the approved package architecture.

Relevant import boundaries are enforced by repository tests.

Do not introduce circular imports, unrelated dependencies or hidden cross-package coupling.

### 6.3 Documentation Contracts

Non-trivial subsystem modules must explain both their functionality and engineering rationale.

The existing documentation contract applies to modules within:

- `tokenizer/`
- `data/`
- `model/`
- `training/`
- `evaluation/`

Required documentation sections are:

```text
Purpose:
Public API:
Invariants:
Failure modes:
See:
```

Modules importing PyTorch also require:

```text
Shapes:
Dtype:
Device:
```

These requirements are checked by:

`tests/test_docs_contract.py`

New modules should follow the same documentation philosophy. Any extension of mandatory validation rules must be implemented and tested explicitly.

### 6.4 Architectural Decisions

Significant architectural choices must be documented in:

[docs/decisions.md](docs/decisions.md)

Decisions use the identifier format:

`D-###`

Relevant source documentation should reference the associated decision identifiers.

Previously approved decisions must not be silently overwritten.

---

## 07 // Testing & Quality Assurance

Testing is required for every substantive code contribution.

### 7.1 Local Validation

Run the project's combined quality checks:

```bash
python scripts/check.py all
```

This command executes the configured groups:

```text
quality
tests
security
```

All applicable checks must pass before a milestone change is accepted.

### 7.2 Unit & Integration Testing

Contributors should:

- Add regression tests for bug fixes.
- Verify edge cases and failure paths.
- Test configuration validation.
- Check parameter and tensor shape assumptions.
- Avoid tests dependent on uncontrolled external services.
- Preserve deterministic CPU test behaviour.
- Use existing test fixtures when suitable.
- Verify that changes do not break unrelated modules.

New model components should be tested against suitable reference implementations where possible.

A passing test suite does not automatically prove model quality.

### 7.3 GPU Testing

GPU-specific tests use:

`@pytest.mark.gpu`

Run them on approved local GPU hardware using:

```bash
pytest -m gpu
```

GPU tests are excluded from ordinary hosted CI under D-010.

Pull requests must state whether relevant GPU tests were:

- Executed and passed
- Executed and failed
- Not run
- Not applicable

Never claim GPU compatibility solely because CPU tests passed.

### 7.4 Numerical Correctness

Machine learning contributions should consider:

- Floating-point precision
- Tensor shapes and device placement
- Non-finite losses and gradients
- Parameter updates
- Attention equivalence
- Checkpoint recovery
- Random-number generator state
- Reproducibility tolerances

CPU and GPU behaviour may differ due to hardware and numerical implementation details.

Measured deviations must be reported rather than concealed.

---

## 08 // Continuous Integration Policy

The required GitHub Actions workflow is:

`.github/workflows/tests.yml`

**Workflow:** `Test`

Required jobs:

| Job | Purpose |
|---|---|
| Quality | Formatting, linting and typing checks |
| Tests — Ubuntu | Linux CPU verification |
| Tests — Windows | Windows CPU verification |
| Security | Configured security checks |

SonarCloud is currently an advisory integration rather than a required CI gate, unless an approved decision changes that status.

### 8.1 Milestone Acceptance

Under D-018, each milestone commit must:

1. Pass `python scripts/check.py all` locally.
2. Pass applicable local GPU tests.
3. Pass all required GitHub CI jobs on the exact commit.
4. Meet the milestone's documented acceptance criteria.
5. Include relevant tests and documentation.
6. Have its verification evidence recorded accurately.

A successful PR preview does not automatically establish that the final merged commit passed required CI.

### 8.2 CI Infrastructure Exceptions

If required GitHub Actions jobs cannot run due to a confirmed infrastructure issue rather than a code failure:

- Record a discrepancy.
- Document the affected checks.
- Preserve local validation evidence.
- Do not misrepresent the unavailable checks as passed.

Under D-018, engineering milestone work may proceed on local verification while the infrastructure discrepancy remains open.

**Formal research experiments remain blocked until the required CI evidence is available.**

### 8.3 Formal Experiment CI Evidence

Every formal experiment must reference required CI results from the exact code commit.

The project provides:

```bash
python scripts/verify_ci.py
```

The script uses the GitHub CLI to retrieve the required workflow evidence for the selected commit, defaulting to `HEAD`.

Evidence is written under:

`runs/ci_evidence/<commit>.json`

The validation contract requires the correct commit, a completed `push` workflow run, and successful required jobs.

Never fabricate, manually reconstruct or falsely modify CI evidence.

---

## 09 // Git Workflow, Commits & Pull Requests

### 9.1 Repository Hygiene

Before beginning work:

1. Confirm the correct repository.
2. Check the active branch and commit.
3. Inspect uncommitted changes.
4. Read the relevant approved milestone scope.
5. Identify affected modules and tests.
6. Avoid overwriting unrelated work.

Do not reset, clean, force-push or otherwise discard another contributor's changes without explicit authorisation.

### 9.2 Commit Standards

Commits should represent one coherent technical change.

Commit messages should explain what changed and, when necessary, why.

Examples:

```text
fix(training): validate checkpoint metadata before resume
test(model): add attention equivalence regression coverage
docs(research): clarify bits-per-byte evaluation methodology
refactor(tokenizer): simplify merge ranking implementation
security(data): reject unsafe dataset paths
```

These are naming examples, not a replacement for the repository's established commit conventions.

### 9.3 Pull Request Requirements

Pull requests should include:

- A concise objective.
- The problem or research requirement being addressed.
- Relevant architectural decisions.
- Files and modules changed.
- Local validation results.
- Applicable GPU test results.
- Security and compatibility considerations.
- Relevant experiment records.
- Dataset provenance, if applicable.
- Known limitations or unresolved issues.

Before requesting review, ensure that:

- The change remains within approved scope.
- Tests and documentation are updated.
- No forbidden artifacts are staged.
- New dependencies are approved.
- Existing functionality has not regressed.
- Formal research claims have suitable evidence.

### 9.4 Review & Approval

Reviewers should assess:

- Technical correctness
- Research validity
- Architectural compatibility
- Code quality
- Security
- Reproducibility
- Test coverage
- Documentation
- Scope compliance

A pull request should not be merged merely because automated checks are green if its scientific claims, security implications or architectural changes remain unresolved.

The Project Owner retains final merge and milestone approval authority.

---

## 10 // Experiment Governance & Research Records

Scientific experimentation must follow the project's approved research methodology.

### 10.1 Experiment Identifiers

Formal experiments use:

`EXP-###`

Variants may use:

`EXP-###-suffix`

Engineering smoke experiments use designated `SMOKE-*` identifiers.

Specialist engineering benchmarks may use `BENCH-*` identifiers.

The experiment record's `kind` must correctly identify its purpose.

### 10.2 Required Record Contents

A formal experiment record must include the applicable schema-required fields for:

- Experiment identity and objective
- Git commit and dirty-tree status
- Verified CI evidence
- Environment and hardware
- Dataset version
- Tokenizer version
- Resolved model configuration
- Full parameter accounting
- Training configuration
- Optimisation settings
- Measured results
- Reproducibility evidence
- Checkpoint resume status
- Known limitations
- Research notes and conclusions

All records must validate against the current repository schema.

Do not invent fields or omit required metadata to force validation.

### 10.3 Missing Measurements

Unmeasured numerical values must use `null` where permitted by the schema.

Do not substitute estimates for observations.

Checkpoint-resume status remains `not_run` unless the approved resume harness was executed.

Passing a training process does not prove checkpoint resume correctness.

### 10.4 Formal Results vs Engineering Diagnostics

Engineering smoke tests confirm targeted aspects of system functionality.

Formal experiments investigate research hypotheses.

Under D-017:

**Smoke experiments cannot be used as evidence of general model quality or architectural superiority.**

Smoke records and formal experiment records must remain distinguishable.

Engineering benchmarks should identify their environment, methodology and limitations.

The experiment ledger is the authoritative location for validated research results.

### 10.5 Generated Research Tables

The research comparison table is generated at:

`experiments/ablations.md`

Use the repository's supported generator:

```bash
python scripts/build_ablation_table.py
```

Never modify the generated comparison table manually.

Generated output must agree with the validated underlying records.

---

## 11 // Benchmarking & Experimental Reproducibility

A benchmark or comparative study must identify what is being measured and under which conditions.

### 11.1 Required Research Controls

Where applicable, report:

- Baseline model
- Experimental variant
- Parameter counts
- Tokenizer and vocabulary
- Dataset and data split
- Training token or byte budget
- Optimiser and scheduler
- Random seed
- Evaluation dataset
- Precision
- Attention backend
- Hardware
- Software environment
- Measurement methodology

Comparisons must not quietly change multiple influential variables while attributing all performance differences to a single architecture change.

### 11.2 Architectural Ablations

Experimental architectural additions require comparison against an appropriate named control, normally `EXP-001` once that baseline has been completed and validated.

Research proposals should explain:

1. The scientific hypothesis.
2. The component being changed.
3. The control configuration.
4. Variables held constant.
5. Parameter-budget differences.
6. Performance and quality metrics.
7. Hardware or computational implications.
8. Expected limitations.
9. Criteria for acceptance or rejection.

Where a parameter budget cannot be matched exactly, the difference must be disclosed and considered in the interpretation.

### 11.3 Tokenizer Comparisons

The primary research tokenizer vocabulary is 16,384 tokens.

Planned vocabulary-size ablations include:

- 8,192
- 12,288
- 24,576
- 32,768

Tokenizer comparisons must follow the approved methodology, including the relevant training-data and budget controls.

Per-token loss alone is not sufficient for cross-vocabulary conclusions.

Bits-per-byte provides an additional normalised metric for comparing tokenisation choices.

### 11.4 Reproducibility Requirements

A reproducible result should be traceable to:

- An exact code revision.
- Validated CI evidence where required.
- Versioned model and tokenizer configurations.
- A versioned dataset.
- Recorded random seeds.
- Identified hardware and software.
- An explicit evaluation procedure.
- A validated experiment record.

Hardware determinism limitations must be documented.

**Reproducibility is established through evidence, not asserted through configuration settings alone.**

---

## 12 // Model Training & Checkpoint Standards

### 12.1 Training Approval

Model training is an explicit research operation.

Training must not begin automatically as part of ordinary code reviews, package installation or CI checks.

Before launching an approved training run, contributors should establish:

- Experiment objective
- Model and dataset configuration
- Expected resource requirements
- Hardware environment
- Training duration or bounded stopping conditions
- Checkpoint strategy
- Failure and recovery behaviour
- Evaluation criteria

Formal runs must satisfy their configured repository and CI evidence requirements.

### 12.2 Numerical Safety

Training code must detect and handle invalid numerical states where required.

Non-finite losses and gradients must not be silently accepted.

Training failures should be recorded and investigated rather than hidden behind retries or suppressed warnings.

### 12.3 Checkpoint Integrity

Checkpoint implementations must preserve the approved D-021 contract.

Its protections include:

- Defined checkpoint format
- Integrity checking
- Safe payload loading
- Atomic writes
- Validated metadata
- Configuration compatibility checks
- Consistent recovery behaviour

New checkpoint implementations must not weaken existing protections.

### 12.4 Deterministic Resume

Under D-012, checkpoint resume claims require approved harness evidence.

Relevant state comparisons include model parameters, optimiser and scheduler state, training counters, RNG states and data-loader progression.

Where GPU numerical behaviour is not bit-exact, report the measured differences using the approved tolerance methodology.

---

## 13 // Dataset Provenance & Data Security

KittyLM's dataset pipeline follows strict provenance and security requirements.

### 13.1 Dataset Source Approval

Every accepted source must have:

- An identifiable origin.
- A declared licence.
- Appropriate usage permissions.
- A documented version or revision.
- Applicable provenance information.

The dataset recipe's `allowed_licenses` policy governs ingestion.

External datasets must not be added without the required approval.

### 13.2 Secret Scanning

Documents must pass the applicable licence validation and secret scanning before acceptance into persisted corpus artifacts.

Under D-006, a document containing a secret-scan finding is dropped rather than partially redacted for dataset inclusion.

Do not introduce private credentials, confidential code or unauthorised personal data into the corpus.

### 13.3 Dataset Manifest Requirements

Dataset manifests must follow the approved schema and include the required hashes, versions, relative paths and provenance metadata.

Avoid embedding absolute local filesystem paths or sensitive environment information.

`DATA_SOURCES.md` is generated from validated manifests and must not be manually altered to misrepresent dataset contents.

### 13.4 Dataset Separation & Leakage

Research datasets should maintain the approved train, validation and test separation.

Document-level splitting follows the established content-hash policy under D-005.

Contributors should investigate exact duplicates, near duplicates and other potential leakage risks where relevant.

Any known limitations in dataset isolation must be reported.

### 13.5 Human-Reviewed Feedback

KittyLM must not automatically train on user feedback or unreviewed external content.

Under D-009, feedback must pass human review before inclusion in a new, curated, versioned dataset.

See:

`kittylm/integration/README.md`

---

## 14 // Security & Repository Artifact Policy

Never commit:

- API tokens or authentication secrets
- Private keys or credentials
- `.env` files containing secrets
- Raw, cleaned or tokenised training datasets
- Private research corpora
- Model checkpoints
- Model weights
- Generated samples
- Run logs
- Local environment files
- Unapproved training artifacts
- Sensitive personal information

Generated research artifacts must remain in their designated local storage locations unless an approved publication process explicitly permits otherwise.

The repository's security tooling includes staged secret scanning and artifact guards.

Tests requiring credential-shaped data should use approved synthetic fixtures assembled at runtime, as demonstrated by the existing `tests/fakes.py` approach.

### Security Vulnerability Reporting

Report vulnerabilities using:

[SECURITY.md](SECURITY.md)

Do not publicly disclose exploitable details or private credentials before appropriate coordinated handling.

### Supply Chain Security

Dependency contributions must:

- Identify the package and proposed version.
- Explain why the dependency is needed.
- Consider licensing and compatibility.
- Review relevant security risks.
- Preserve repeatable development environments.
- Pass the required verification checks.

Automated dependency pull requests must receive the same validation as other code changes.

A successfully merged dependency update is not automatically evidence that the resulting environment is functional.

---

## 15 // AI-Assisted Engineering Contributions

KittyLM permits responsible use of AI-assisted software development and research tools.

Examples include Claude, ChatGPT and other authorised engineering assistants.

AI-generated work must satisfy the same standards as human-authored contributions.

### 15.1 Contributor Responsibilities

When submitting AI-assisted work:

- Review generated code.
- Verify technical assumptions.
- Run appropriate tests.
- Check for insecure patterns.
- Confirm compatibility with project decisions.
- Verify citations and external references.
- Record relevant limitations.
- Disclose material AI assistance where required.

### 15.2 Research Claims

AI-generated benchmark claims, measurements and experiment summaries must never be treated as verified evidence without supporting records.

Language model output is not an authoritative source of execution results.

No assistant may claim that a tool, test, experiment or CI workflow was executed unless it has appropriate evidence.

### 15.3 Human Oversight

AI assistants may advise, implement authorised tasks and assist with review.

They do not independently approve:

- Architecture changes
- New training datasets
- Formal experiments
- Major dependency changes
- Security policy changes
- Releases or public publication

Project approval remains human-controlled.

---

## 16 // Proposing Research or Architecture Changes

Significant experimental changes should begin with an issue or documented proposal.

### Proposal Template

**Research Proposal**

| Field | Description |
|---|---|
| Title | Concise name of the proposed research |
| Research question | What is being investigated? |
| Hypothesis | Expected effect and technical reasoning |
| Baseline | Existing model or experiment used as control |
| Proposed change | Single principal component being tested |
| Variables | What changes and what remains constant |
| Parameter budget | Expected model size and changes |
| Dataset | Version and provenance |
| Metrics | Measurements used for evaluation |
| Resources | Expected hardware and compute requirements |
| Risks | Numerical, compatibility, safety or security risks |
| Acceptance criteria | Conditions for evaluating the hypothesis |
| Plan impact | Whether a formal revision is required |

### Proposed Research Workflow

1. Submit the hypothesis and design.
2. Review feasibility and scope.
3. Identify the correct baseline.
4. Obtain approval for any required plan revision.
5. Implement behind established interfaces where appropriate.
6. Add unit and regression tests.
7. Complete engineering verification.
8. Run the authorised experiment.
9. Validate the experiment record.
10. Regenerate applicable result tables.
11. Report outcomes, limitations and uncertainty.

Proposing an advanced architecture does not grant permission to introduce it into the current baseline prematurely.

---

## 17 // Documentation & Reporting Requirements

Documentation should accurately describe implemented behaviour, planned functionality and known limitations.

### 17.1 Evidence Classification

Technical reports should distinguish:

- **VERIFIED:** Directly supported by tests, measurements or inspected evidence.
- **REPORTED:** Communicated but not independently verified.
- **INFERRED:** Supported by reasoning and stated assumptions.
- **PROPOSED:** Suggested future work.
- **UNKNOWN:** Insufficient evidence.
- **BLOCKED:** Prevented by an unresolved prerequisite or restriction.

### 17.2 Milestone Reports

Substantial changes should be accompanied by a structured engineering report covering:

1. Objective and approved scope.
2. Initial repository and environment state.
3. Implemented changes.
4. Files and modules affected.
5. Local verification.
6. GitHub CI results.
7. GPU validation where relevant.
8. Measured outcomes.
9. Failures and regressions.
10. Risks and uncertainties.
11. Relevant commits and artifacts.
12. Outstanding approvals and recommended next steps.

Use exact references whenever possible.

Do not imply that proposed or unverified work is complete.

### 17.3 Failed Experiments

Failed experiments should be documented accurately.

Where records are produced, preserve the applicable configuration and failure evidence.

A failed result should not be removed solely because it contradicts the original hypothesis.

Corrections and superseded conclusions should remain traceable.

---

## 18 // Contribution Acceptance Checklist

Before requesting final review, verify the following.

### Engineering

- [ ] The change is within approved scope.
- [ ] The current repository state has been inspected.
- [ ] Existing architectural boundaries are preserved.
- [ ] Code is readable, typed and documented appropriately.
- [ ] Relevant regression tests have been added.
- [ ] Local quality and security checks pass.
- [ ] Applicable GPU tests have been executed or marked not run.

### Research

- [ ] Scientific claims are supported by appropriate evidence.
- [ ] Relevant baseline comparisons are identified.
- [ ] Parameter accounting is complete where required.
- [ ] Experimental controls are documented.
- [ ] Formal results have validated experiment records.
- [ ] Required exact-commit CI evidence is available.
- [ ] Generated research tables are synchronised.
- [ ] Unknowns and limitations are disclosed.

### Security & Provenance

- [ ] No credentials or sensitive artifacts are committed.
- [ ] Dataset sources have appropriate licences and provenance.
- [ ] No unauthorised external data has been introduced.
- [ ] New dependencies have been reviewed and authorised.
- [ ] Checkpoint and serialization protections remain intact.
- [ ] Project security and responsible-use policies are respected.

### Review & Governance

- [ ] The change has a clear purpose.
- [ ] The commit and pull request descriptions are accurate.
- [ ] Significant decisions are documented.
- [ ] Unresolved discrepancies are reported.
- [ ] Required approvals have been obtained.
- [ ] No unverified capability is represented as complete.

**A contribution is accepted only when its applicable technical, scientific, security and governance requirements have been satisfied.**

---

## 19 // Related Project Documentation

| Document | Purpose |
|---|---|
| [README.md](README.md) | Project overview, architecture and roadmap |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community behaviour and scientific professionalism |
| [SECURITY.md](SECURITY.md) | Vulnerability disclosure and security handling |
| [docs/architecture.md](docs/architecture.md) | Architecture and component responsibilities |
| [docs/decisions.md](docs/decisions.md) | Approved architectural decisions |
| [docs/discrepancies.md](docs/discrepancies.md) | Engineering discrepancies and resolution evidence |
| [docs/limitations.md](docs/limitations.md) | Model and research limitations |
| [docs/responsible-use.md](docs/responsible-use.md) | Responsible AI research and use |
| [docs/safety.md](docs/safety.md) | Safety and security controls |
| [DATA_SOURCES.md](DATA_SOURCES.md) | Dataset provenance |
| [experiments/](experiments/) | Experiment and benchmark records |

---

## 20 // Final Statement

KittyLM is not simply an exercise in writing machine learning code.

It is a long-term effort to understand the engineering and scientific foundations of modern language models.

Every contribution should strengthen at least one of the project's fundamental goals:

- A more correct implementation.
- A more reproducible experiment.
- A more secure development process.
- A clearer understanding of model behaviour.
- A better documented scientific result.
- A more maintainable research platform.

We value curiosity, technical discipline, transparent experimentation and responsible innovation.

Contributors are encouraged to think independently, challenge assumptions and explore meaningful research questions while respecting the project's engineering standards and established development scope.

**The objective is not to produce impressive claims. It is to produce research and software that can withstand careful examination.**

### `KITTYLM // BUILD. MEASURE. LEARN. EVOLVE.`

*Engineering with purpose. Research with integrity. Progress through evidence.*

**© 2026 KrazyKitty — KittyLM Research & Development**
