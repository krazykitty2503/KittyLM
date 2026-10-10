# KittyLM // Third-Party Notices

**Open-Source Compliance · Software Attribution · Research Licensing · Dependency Transparency**

**Document:** `THIRD_PARTY_NOTICES.md`  
**Project:** KittyLM — Independent Language Model Research & Development  
**Project Owner:** KrazyKitty  
**Document Version:** 1.0  
**Last Updated:** 10 October 2026  
**Primary Source-Code Licence:** Apache License 2.0

---

## 01 // Purpose & Licensing Principles

KittyLM is an independent artificial intelligence and language model research project focused on reproducible software engineering, experimental neural architectures, transparent evaluation and responsible AI development.

KittyLM's original source code is licensed under the **Apache License, Version 2.0**.

The project uses third-party software libraries, development tools, research references and established technical standards. These components retain their respective copyright ownership and applicable licences.

This document identifies the third-party components currently declared by KittyLM, records available licence information and explains how dependencies and external research materials are handled.

### 1.1 Core Licensing Principles

KittyLM follows these principles:

- Respect third-party copyright and licence requirements.
- Preserve applicable attribution and redistribution notices.
- Distinguish original KittyLM software from external components.
- Maintain traceability between dependency declarations and reviewed licence information.
- Avoid representing third-party software as originally developed by KittyLM.
- Review licensing implications before adding, modifying or redistributing external components.
- Keep dataset, documentation and model-weight licensing separate from the software licence.
- Record uncertainty rather than inventing missing licence information.

**KittyLM's Apache-2.0 licence does not replace, override or relicense independently developed third-party components.**

### 1.2 Scope

This document covers:

- Direct runtime dependencies.
- Development and testing tools.
- Python packaging and build-system requirements.
- Third-party documentation incorporated into the project.
- Transitive dependency attribution boundaries.
- Research datasets and future model artifacts.
- Future software distribution and licensing verification.

This is a maintained attribution register, not a complete software bill of materials or an exhaustive legal audit of every distributed package.

---

## 02 // Software Licensing Overview

The repository maintains separate licensing documentation for different categories of project material.

| Component | Applicable licensing arrangement | Reference |
|---|---|---|
| Original KittyLM source code | Apache-2.0 | [LICENSE](LICENSE) |
| KittyLM project attribution | Copyright and attribution notices | [NOTICE](NOTICE) |
| Research and engineering documentation | CC BY 4.0, subject to stated exceptions | [docs/LICENSE.md](docs/LICENSE.md) |
| Future KittyLM model weights | Intended Apache-2.0 release policy | [MODEL_LICENSE.md](MODEL_LICENSE.md) |
| Training datasets | Applicable individual source licences and permissions | [DATA_SOURCES.md](DATA_SOURCES.md) |
| Third-party software | Original upstream licences | This document |
| Adapted external documents | Original applicable licences and attribution requirements | Section 06 |

The existence of a licensing policy does not imply that a future model, dataset or artifact has already been released.

### 2.1 Apache License 2.0

KittyLM's original code is distributed under Apache-2.0.

The legal terms are contained in the repository's root-level `LICENSE` file.

Official licence text:

https://www.apache.org/licenses/LICENSE-2.0

### 2.2 Third-Party Ownership

Third-party libraries remain the work of their respective authors and copyright holders.

Using a dependency does not transfer ownership of that dependency to KittyLM.

Likewise, installing a library does not automatically grant permission to redistribute every bundled asset under KittyLM's own software licence.

---

## 03 // Runtime Dependencies

Runtime dependencies are declared in the project's `pyproject.toml`.

The current dependency declarations use lower version bounds rather than exact package pins.

Installed versions can therefore vary between local research environments and GitHub Actions.

### 3.1 Direct Runtime Dependency Register

| Package | Declared version requirement | Previously recorded inspected version |
|---|---|---|
| [PyTorch](https://github.com/pytorch/pytorch) (`torch`) | `>=2.4` | `2.13.0+rocm10.0.0` |
| [NumPy](https://github.com/numpy/numpy) (`numpy`) | `>=1.26` | `2.5.3` |
| [PyYAML](https://github.com/yaml/pyyaml) (`pyyaml`) | `>=6.0` | `6.0.3` |
| [regex](https://github.com/mrabarnett/mrab-regex) (`regex`) | `>=2024.0` | `2026.9.10` |

The previously inspected versions are carried forward from the earlier KittyLM third-party notice.

They represent historical development-environment observations and are not newly verified installed-package measurements.

### 3.2 Previously Recorded Licence Metadata

| Package | Licence information recorded in the previous environment |
|---|---|
| PyTorch | `Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND MIT` |
| NumPy | `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0` |
| PyYAML | `MIT` |
| regex | `Apache-2.0 AND CNRI-Python` |

These entries preserve licence metadata previously recorded by KittyLM.

They must not be interpreted as a complete independent audit of all source files, binary components, transitive libraries or the exact currently installed wheels.

Complex licence expressions may describe several separately licensed components included in one distribution.

Where authoritative upstream licensing or package-specific notices differ from an earlier record, the discrepancy must be reviewed and the register updated with evidence.

### 3.3 PyTorch and Hardware-Specific Builds

KittyLM uses PyTorch for neural network implementation, automatic differentiation, optimisation and GPU-accelerated computing.

The previously recorded local research environment used an AMD ROCm-enabled PyTorch distribution.

GitHub Actions uses a CPU-compatible PyTorch installation.

These environments may install different package builds and dependencies.

Therefore:

- GPU and CPU package inventories must not be assumed identical.
- Hardware-specific distributed components may have additional applicable licence notices.
- An audited local environment does not automatically establish the licensing contents of a different CI installation.
- The exact installed distribution should be inspected before redistribution.

### 3.4 Research Reproducibility

Formal experiments should record the actual installed software environment, including relevant dependency versions.

A declared minimum version is not equivalent to the version used for an experiment.

Where package versions influence numerical behaviour, performance or model reproducibility, those differences should be disclosed.

---

## 04 // Development & Testing Dependencies

KittyLM uses third-party tools for automated testing, formatting, static analysis, dependency auditing and package construction.

These tools are declared in the optional development dependency group.

### 4.1 Direct Development Dependency Register

| Package | Version declared in `pyproject.toml` | Licence information |
|---|---|---|
| [pytest](https://github.com/pytest-dev/pytest) | `9.1.1` | MIT — previously recorded |
| [Ruff](https://github.com/astral-sh/ruff) | `0.16.10` | MIT — previously recorded |
| [mypy](https://github.com/python/mypy) | `2.4.0` | MIT — previously recorded |
| [pip-audit](https://github.com/pypa/pip-audit) | `2.10.1` | Apache-2.0 — upstream project |
| [build](https://github.com/pypa/build) | `1.6.1` | MIT — upstream project |

The version column reflects current package declarations, not proof that every version is installed in the local environment.

Earlier project records listed Ruff `0.16.7` and mypy `2.3.1`. These have been superseded by the development requirements listed above.

Package-specific licence metadata should be rechecked when dependency versions are updated.

### 4.2 Development Tool Purpose

| Tool | Role within KittyLM |
|---|---|
| pytest | Unit, integration and regression testing |
| Ruff | Python formatting, linting and code-quality checks |
| mypy | Static type analysis |
| pip-audit | Identification of known package vulnerabilities |
| build | Python source distribution and wheel construction |

The inclusion of development tools does not imply that they are bundled into KittyLM's runtime package.

### 4.3 Security Auditing and Licensing

Dependency vulnerability scanning and licence compliance are distinct activities.

A package may have no known security advisories but still carry redistribution, attribution or licence obligations.

Likewise, a package's valid open-source licence does not establish that it is free from vulnerabilities.

KittyLM should assess both security and licensing before accepting significant dependency changes.

---

## 05 // Python Build-System Dependencies

KittyLM's Python packaging configuration declares additional build-system dependencies.

These are separate from ordinary runtime dependencies and the optional developer tool group.

### 5.1 Build-System Register

| Component | Current declaration | Purpose |
|---|---|---|
| [setuptools](https://github.com/pypa/setuptools) | `>=77.0.3` | Build backend |
| [wheel](https://github.com/pypa/wheel) | No explicit version pin | Wheel-building support |

The project declares:

```toml
[build-system]
requires = ["setuptools>=77.0.3", "wheel"]
build-backend = "setuptools.build_meta"
```

The exact installed versions and applicable licence metadata for these build-system dependencies have not been recorded in this notice.

They should be verified during a formal dependency licence inventory.

### 5.2 Build Artifact Review

Before publishing or distributing KittyLM packages, maintainers should inspect the generated source distribution and wheel.

The review should verify:

- The applicable software licence is included.
- Required notices and attribution are preserved.
- Package metadata accurately identifies the project licence.
- No prohibited research artifacts are included.
- Third-party files are not accidentally presented as original KittyLM code.
- Packaging behaviour agrees with the approved release configuration.

The presence of a file in the source repository does not guarantee that it is included in every packaged artifact.

---

## 06 // Documents Adapted from Third Parties

Some KittyLM documentation incorporates established external legal or community-governance material.

These sources must receive appropriate attribution.

| Document | Original source | Applicable licence or attribution |
|---|---|---|
| `LICENSE` | Apache License, Version 2.0 | Apache-2.0 |
| `CODE_OF_CONDUCT.md` | Contributor Covenant, Version 2.0 | CC BY 4.0 attribution |
| `NOTICE` | KittyLM project attribution and licensing summary | Project-authored informational notice |

### 6.1 Apache License

The project's root-level `LICENSE` contains the Apache License 2.0 legal terms.

Original source:

https://www.apache.org/licenses/LICENSE-2.0

The canonical legal terms should be preserved without substantive modification.

Project-specific attribution belongs in the appropriate copyright notices, file headers and accompanying attribution documentation.

### 6.2 Contributor Covenant

KittyLM's Code of Conduct is adapted from the Contributor Covenant, Version 2.0.

The adaptation introduces additional project-specific provisions concerning:

- Scientific integrity.
- Responsible AI research.
- Engineering professionalism.
- Software security.
- Dataset provenance.
- AI-assisted contributions.
- Community governance.

Original source:

https://www.contributor-covenant.org/version/2/0/code_of_conduct.html

The project must preserve the required attribution and clearly distinguish its additional policies from the original Contributor Covenant.

### 6.3 Documentation Licensing

Original KittyLM documentation is governed by the repository's documentation licence unless a file states otherwise.

See:

[docs/LICENSE.md](docs/LICENSE.md)

A document incorporating third-party material may have separate obligations that must be respected independently.

---

## 07 // Transitive Dependencies & External Components

The direct dependency tables do not represent the full dependency tree.

Installing PyTorch, NumPy or other packages may also install additional software components.

These components can include:

- Python libraries.
- Numerical computing libraries.
- Native binary extensions.
- Hardware-specific runtime components.
- Compiler or build utilities.
- Libraries bundled in platform-specific wheels.
- Other upstream software required by the dependency.

### 7.1 Transitive Dependency Policy

Transitive dependencies retain their original licences and copyright notices.

KittyLM does not claim ownership of external software merely because it is required by a direct dependency.

When relevant to an intended distribution, maintainers should:

1. Identify the resolved dependency tree.
2. Record the exact package versions and distribution artifacts.
3. Inspect available licence metadata and licence files.
4. Identify attribution and redistribution obligations.
5. Resolve unclear licensing conditions.
6. Preserve required third-party notices.
7. Retain appropriate audit evidence.

### 7.2 Licensing Metadata Limitations

Package metadata may be incomplete, inconsistent or too broad to describe every independently licensed component.

An SPDX expression can combine several applicable licences.

A legacy licence classifier is not necessarily equivalent to a complete SPDX licence expression.

The authoritative terms are the applicable upstream licences and notices for the components actually used or distributed.

### 7.3 Vendoring and Redistribution

KittyLM's current development approach installs third-party Python dependencies from their respective distributions rather than maintaining copied dependency source trees as part of its own codebase.

Future deployment methods may change the distribution boundary.

Examples include:

- Container images.
- Bundled Python executables.
- Packaged desktop applications.
- Deployment archives containing dependencies.
- Copied or modified third-party source code.
- Model inference distributions with embedded runtimes.

Such distributions require a separate assessment of the software and licence materials actually included.

A decision to vendor software must not be made without appropriate project approval.

---

## 08 // Research Datasets & External Training Sources

### 8.1 Current Dataset Status

**No dataset has been built yet.**

KittyLM's curated `local-v1` training corpus and full dataset ingestion pipeline remain planned under Milestone F.

No formally approved external training sources are currently recorded in the project dataset registry.

Engineering fixtures used for software testing are not equivalent to an accepted pretraining corpus.

### 8.2 Per-Source Licensing

Training data retains its respective licensing, copyright, provenance and permission requirements.

The Apache-2.0 licence applied to KittyLM's source code does not independently grant permission to use, redistribute or publish third-party training material.

Before accepting a source, KittyLM requires the applicable review of:

- Origin and ownership.
- Licence terms.
- Research-use permissions.
- Redistribution restrictions.
- Privacy and sensitive information.
- Provenance and versioning.
- Project approval.

### 8.3 Dataset Provenance Registry

Approved sources will be documented through the dataset provenance system when its tooling has been implemented.

The intended future register records source licensing and processing outcomes from validated manifests.

See:

[DATA_SOURCES.md](DATA_SOURCES.md)

The full generated registry is planned; it should not be represented as already operational.

### 8.4 Independent Research Projects

External research datasets, including those shared by collaborators or hosted on model and dataset platforms, remain subject to their own licensing and permission requirements.

Discussion, inspection or evaluation of an external dataset does not automatically authorise its inclusion in KittyLM training.

---

## 09 // Model Weights & Future Research Artifacts

KittyLM's intended model-weight licensing policy is documented separately.

See:

[MODEL_LICENSE.md](MODEL_LICENSE.md)

### 9.1 Model Weight Status

No formal pretrained KittyLM model weights have been released under the current research programme.

The project's current intended policy is to release future approved KittyLM model weights under Apache-2.0.

This intention does not constitute an automatic release commitment.

### 9.2 Release Requirements

Before publishing model weights, the project should review:

- Ownership and licensing rights.
- Training source permissions.
- Dataset provenance.
- Experiment reproducibility.
- Model configuration and tokenizer compatibility.
- Known limitations.
- Security and privacy risks.
- Relevant third-party component obligations.
- Applicable model-release documentation.

### 9.3 Independent Licensing

Model weights, datasets, tokenizer assets, software libraries and accompanying documentation may have different licensing requirements.

A licence applied to one component must not be assumed to cover all other components.

---

## 10 // Open-Source Compliance & Dependency Updates

KittyLM's open-source compliance process should be integrated into its existing engineering workflow.

### 10.1 Dependency Change Review

When adding or changing a dependency, maintainers should document:

1. Package identity and upstream source.
2. The proposed dependency version or range.
3. The technical reason for the change.
4. Available licence evidence.
5. Security and maintenance implications.
6. Compatibility with the existing software architecture.
7. Whether the component will be redistributed.
8. Any required updates to this notice or other licensing documents.

### 10.2 Version Accuracy

The development dependency versions in this document must be reconciled with `pyproject.toml` whenever they change.

Historical local-environment measurements must remain identifiable as historical evidence.

A pinned requirement is not the same as a verified installed version.

### 10.3 Research Environment Records

For formal reproducibility, dependency versions used during a model experiment should be recorded in the applicable research environment evidence.

The scientific record must refer to the packages actually used during execution.

### 10.4 Automated Compliance Improvements

Potential future improvements include:

- Machine-readable dependency inventories.
- Software bills of materials (SBOMs).
- Licence metadata verification.
- Transitive dependency reporting.
- Release artifact inspection.
- Checks for outdated dependency notices.
- Auditable licence-review records.

These are proposed enhancements, not claims of currently implemented automation.

Any new CI enforcement or dependency tooling requires approval under the project's development governance.

---

## 11 // Redistribution, Attribution & Legal Notices

### 11.1 Original KittyLM Code

Redistribution of original KittyLM source code must comply with Apache-2.0.

The complete legal terms are provided in:

[LICENSE](LICENSE)

### 11.2 Project NOTICE

The repository contains:

[NOTICE](NOTICE)

This file provides project attribution and information about the separate licensing arrangements.

It does not alter the terms of Apache-2.0 or third-party licences.

Applicable notices must be retained when redistribution conditions require them.

### 11.3 Third-Party Licence Materials

If KittyLM distributes external software or copied third-party code, maintainers must identify and comply with the relevant licence-text, notice and attribution requirements.

This document is not a replacement for any full third-party licence text that must accompany a distribution.

### 11.4 Documentation and Attribution

Original KittyLM documentation and adapted third-party documents must be attributed according to their applicable licensing terms.

Attribution should not imply that upstream projects endorse, sponsor or maintain KittyLM.

### 11.5 No Implied Endorsement

References to third-party frameworks, libraries, research projects and software tools identify their technical relationship to KittyLM.

They do not imply endorsement, certification, affiliation or sponsorship unless separately established.

---

## 12 // Compliance Verification & Known Limitations

This document records the available licensing evidence, but several boundaries remain important.

| Area | Evidence status | Limitation |
|---|---|---|
| Direct runtime dependencies | Declared in `pyproject.toml` | Resolved versions vary by environment |
| Earlier runtime licence expressions | Preserved from the prior notice | Exact distributions have not been re-audited here |
| Development dependency versions | Current declarations inspected | Installed versions not independently verified |
| Development licence metadata | Historical metadata and selected upstream references | Exact release-specific licence files should be checked |
| Build-system dependencies | Declared in `pyproject.toml` | Full installed licence inventory pending |
| Transitive dependencies | Not exhaustively listed | Additional licences may apply |
| Dataset provenance | No accepted training corpus | Generated registry remains planned |
| Model weights | No public trained weights recorded | Future release review required |
| Distribution artifacts | Packaging rules declared | Licence and notice inclusion must be verified on actual builds |

### 12.1 Resolving Discrepancies

If a licensing discrepancy is discovered:

- Identify the affected package or artifact.
- Preserve the relevant version and source evidence.
- Review the applicable upstream licence.
- Determine whether existing distribution or use is affected.
- Propose an appropriate correction.
- Update the register after review.
- Record significant project-governance implications where required.

Do not silently rewrite historical licence observations as if they were new measurements.

### 12.2 Publication Readiness

Prior to a stable software or model release, KittyLM should confirm that all required licences, notices and source attributions are accurate for the material actually being distributed.

Licensing compliance must be considered alongside security, scientific reproducibility and engineering quality.

---

## 13 // Related Project Documentation

| Document | Purpose |
|---|---|
| [LICENSE](LICENSE) | Original software licence |
| [NOTICE](NOTICE) | Project attribution |
| [README.md](README.md) | Project overview |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development and research contribution standards |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community standards and adapted attribution |
| [SECURITY.md](SECURITY.md) | Vulnerability and incident reporting |
| [MODEL_LICENSE.md](MODEL_LICENSE.md) | Intended licensing of future model weights |
| [DATA_SOURCES.md](DATA_SOURCES.md) | Dataset licensing and provenance |
| [docs/LICENSE.md](docs/LICENSE.md) | Research documentation licence |
| [docs/decisions.md](docs/decisions.md) | Architectural and engineering decisions |

---

## 14 // Final Statement

KittyLM supports open scientific research and software engineering while recognising the rights and contributions of the wider open-source ecosystem.

Third-party libraries, tools and research materials make modern machine learning possible.

Respecting their licences, preserving appropriate attribution and accurately documenting dependencies are essential parts of responsible engineering.

The project is committed to maintaining clear licensing boundaries, traceable dependencies and an honest record of external contributions.

**Open research depends on responsible attribution. Reproducible engineering depends on transparent dependencies.**

### `KITTYLM // OPEN RESEARCH. RESPECTED LICENCES. VERIFIED ENGINEERING.`

*Building independently. Learning collaboratively. Respecting every contribution.*

**© 2026 KrazyKitty — KittyLM Research & Development**
