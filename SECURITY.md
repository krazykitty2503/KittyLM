# KittyLM // Security Policy

**Secure Engineering · Responsible Disclosure · Dataset Integrity · Model Safety · Research Accountability**

**Document:** `SECURITY.md`  
**Project:** KittyLM — Independent Language Model Research & Development  
**Project Owner:** KrazyKitty  
**Policy Version:** 1.0  
**Last Updated:** 10 October 2026  
**Repository:** [krazykitty2503/kittylm](https://github.com/krazykitty2503/kittylm)

---

## 01 // Security Principles & Scope

KittyLM is an independent artificial intelligence and language model research project focused on original model engineering, reproducible experimentation and responsible AI development.

Security is a fundamental part of KittyLM's architecture and scientific integrity.

The project uses source code, neural network implementations, training configurations, experimental records, checkpoints, datasets and development infrastructure. Each component introduces potential security, privacy, integrity or reproducibility risks.

This policy establishes how security concerns should be reported, assessed, investigated and remediated.

### 1.1 Security Commitments

KittyLM follows these guiding principles:

- **Security by design:** Consider security during architecture and implementation, not only after release.
- **Responsible disclosure:** Protect affected systems and users while vulnerabilities are investigated.
- **Least privilege:** Limit access and permissions to what is required.
- **Defence in depth:** Use multiple independent safeguards wherever practical.
- **Data protection:** Prevent unauthorised disclosure of secrets, private information and research artifacts.
- **Research integrity:** Maintain trustworthy experiment records, dataset provenance and checkpoint identities.
- **Transparent reporting:** Distinguish implemented protections from proposed or unverified safeguards.
- **Human oversight:** Require authorised review for sensitive security operations.

Security controls reduce risk but do not guarantee that vulnerabilities, data exposure or model failures cannot occur.

### 1.2 Covered Components

This policy applies to KittyLM-controlled assets and workflows, including:

- Source code and Python packages.
- Git repositories and development branches.
- GitHub Actions and repository automation.
- Dependencies and build infrastructure.
- Tokenisation and special-token handling.
- Dataset acquisition, validation and processing.
- Model training and evaluation.
- Checkpoint storage, loading and recovery.
- Model generation and research outputs.
- Experiment records and provenance manifests.
- Authorised integrations and future deployment systems.

Third-party services, external datasets and unrelated infrastructure remain subject to their own security and disclosure policies.

---

## 02 // Reporting Security Vulnerabilities

Security concerns should be reported privately to the KittyLM project maintainer.

**Security reporting contact:**

`security@krazykitty.dev`

Please use a descriptive email subject such as:

`[KittyLM Security] Checkpoint validation vulnerability`

Do not disclose an exploitable vulnerability through a public GitHub issue or discussion while it remains unmitigated.

### 2.1 What to Include

Where available, a useful report contains:

- A concise vulnerability summary.
- The affected component or file.
- The relevant version, branch or commit.
- Preconditions required to reproduce the behaviour.
- A minimal, safe reproduction procedure.
- The observed behaviour.
- The expected secure behaviour.
- An assessment of potential impact.
- Suggested mitigations, if known.

Reports may be submitted even when every technical detail is not yet understood.

### 2.2 Sensitive Information

**Never include live secrets, authentication credentials, private keys or unnecessary personal data in a security report.**

Where evidence contains sensitive information:

- Describe the affected location without reproducing the value.
- Use synthetic, non-functional examples where possible.
- Avoid attaching private datasets, credentials or complete confidential logs.
- Inform the maintainer that restricted evidence exists.
- Agree on an appropriate secure evidence-transfer method before sharing it.

Do not upload live secrets as GitHub attachments, paste them into public discussions or include them in automated issue templates.

### 2.3 Reporting Channels

Email is the currently documented security contact.

GitHub Private Vulnerability Reporting may be considered if it is enabled and verified for the repository.

Do not assume that a GitHub security feature is operational merely because it is mentioned in project documentation.

Community behaviour concerns unrelated to technical security should follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## 03 // Supported Versions

KittyLM is in active pre-release research development.

The current package series is `0.x`, and development should not be interpreted as providing production-level support guarantees.

| Version or branch | Security support |
|---|---|
| Latest `main` commit | Supported for accepted security fixes |
| Earlier `0.x` revisions | No maintained security-backport commitment |
| Historical milestones | Research and archival reference only |
| Experimental branches | Reviewed within their approved development scope |
| Future stable releases | Policy to be defined when released |

Security fixes are normally developed against the latest supported `main` revision.

Historical or experimental code may contain known limitations and should not be presumed suitable for production environments.

A fix to `main` does not automatically update older clones, branches, environments or model artifacts.

---

## 04 // Report Categories

KittyLM accepts security reports across its software and research infrastructure.

| Category | Examples | Initial response |
|---|---|---|
| Repository security | Unsafe scripts, CI permissions, workflow injection | Assess impact, restrict exposure, add regression coverage |
| Dataset contamination | Unauthorised, unlicensed, confidential or sensitive data | Stop affected ingestion, exclude material, review downstream artifacts |
| Accidental secret inclusion | Credentials in Git, manifests, logs, checkpoints or outputs | Activate secret-inclusion runbook |
| Model security | Special-token injection, sensitive-data memorisation, unsafe output persistence | Reproduce safely, evaluate exposure, document mitigation |
| Dependency vulnerabilities | Vulnerable packages, malicious dependencies, supply-chain issues | Verify applicability, update or document mitigation |
| Checkpoint security | Unsafe deserialisation, corrupted metadata, compatibility bypass | Isolate artifact, reproduce, strengthen validation |
| Training integrity | Tampered datasets, compromised records, unauthorised experiment changes | Preserve evidence, suspend affected research claims |
| Access and permissions | Excessive privileges or unintended artifact exposure | Restrict access, review scope, remediate permissions |

A report's category does not automatically determine severity.

Severity depends on exploitability, exposure, impact, affected assets and the effectiveness of existing mitigations.

### 4.1 Model Behaviour vs Security Vulnerabilities

Not every incorrect, unsafe or unexpected model response constitutes an exploitable software vulnerability.

Model behaviour reports should identify the relevant security boundary or demonstrable risk.

Examples include:

- A tokenizer accepting unauthorised control tokens.
- An inference output leaking sensitive training material.
- A model artifact bypassing validation.
- A future agent integration performing an unauthorised action.

Ordinary model-quality limitations should generally be documented through evaluation and responsible-use procedures.

---

## 05 // Vulnerability Triage & Response

Reports will be reviewed according to available maintainer capacity, potential harm and technical evidence.

KittyLM is currently a small independent research project and does not advertise a guaranteed incident-response service-level agreement.

### 5.1 Severity Assessment

| Severity | General interpretation |
|---|---|
| Critical | Active credential compromise, unauthorised code execution or severe exposure of protected assets |
| High | Significant security boundary bypass with a credible exploitation path |
| Medium | Meaningful security weakness requiring specific conditions or limited access |
| Low | Limited-impact issue or defence-in-depth weakness |
| Informational | Security observation without a confirmed exploitable impact |

These classifications guide prioritisation rather than guarantee specific resolution times.

### 5.2 Response Workflow

The general incident-handling process is:

1. Receive and acknowledge the report when reasonably practicable.
2. Assess the reported behaviour and available evidence.
3. Identify affected assets, versions and security boundaries.
4. Contain any immediate exposure.
5. Determine severity and likely impact.
6. Develop and test an appropriate mitigation.
7. Validate the fix against regression tests and relevant security checks.
8. Document the outcome and remaining limitations.
9. Coordinate disclosure where appropriate.

The maintainer may request additional technical information.

The reporter should not be asked to disclose unnecessary sensitive information to prove the issue.

### 5.3 Research Integrity Impact

When a vulnerability affects training datasets, checkpoint validity or experiment records, the investigation must consider whether published or recorded research conclusions remain reliable.

Affected results should be clearly identified and their status documented.

An incident involving research infrastructure may require more than a software patch.

---

## 06 // Secret-Inclusion Incident Runbook

**Any exposed live credential must be treated as potentially compromised immediately.**

The first priority is to prevent further unauthorised use, not merely to remove the visible string.

### Step 1 — Revoke or Rotate the Credential

Revoke, rotate or disable the credential through the issuing service using an authorised account.

If the person investigating does not control the credential, notify its owner or responsible administrator through an appropriate secure channel.

Do not delay containment while preparing a repository cleanup.

Deleting a credential from a file does not undo its disclosure.

### Step 2 — Stop Further Exposure

Identify and suspend affected operations where necessary.

Potential actions include:

- Pausing affected dataset ingestion.
- Restricting access to exposed artifacts.
- Disabling compromised integrations.
- Preventing publication of affected logs or samples.
- Suspending distribution of contaminated checkpoints.
- Stopping automated processes that may repeat the leak.

Do not copy the exposed value into incident notes.

### Step 3 — Identify the Exposure Scope

Determine whether the secret appears in:

- Git working files or committed history.
- CI logs or build artifacts.
- Dataset source documents.
- Dataset manifests.
- Experiment records.
- Model checkpoints.
- Generated samples.
- Training metrics or debug logs.
- External storage or previously published material.

Consider relevant copies, caches, clones and downstream artifacts.

A secret scanner finding is evidence of a potential problem, not proof that every copy has been identified.

### Step 4 — Remove or Exclude the Source

For an affected repository file, remove the credential from the current tracked content and implement appropriate regression protections.

For dataset contamination, apply the approved exclusion procedure.

Under D-006, a document with a secret-scan finding must be excluded in full from the accepted corpus.

Do not treat partial redaction as an acceptable replacement for the approved ingestion rule.

Retain only safe evidence needed for the incident record.

### Step 5 — Invalidate Affected Dataset Versions

When contamination affects a built dataset:

- Identify affected source and dataset versions.
- Exclude the compromised source or document.
- Increment `recipe_version` as required by the approved data pipeline.
- Rebuild the dataset under a new `dataset_version`.
- Validate the resulting provenance manifests.
- Prevent further use of the contaminated dataset version.

These dataset pipeline actions apply once the relevant Milestone F tooling exists.

They must not be reported as completed before implementation and execution.

### Step 6 — Assess Experiments and Checkpoints

Identify every experiment or checkpoint potentially derived from the affected data.

Document the incident and compromised status in the applicable experiment record notes or incident tracking system, using supported schema fields.

Do not invent an unsupported record status field.

Affected model checkpoints may have memorised sensitive values even when they do not visibly contain the source document.

Restrict or quarantine suspect checkpoints pending authorised assessment.

Delete or securely dispose of affected artifacts when approved and appropriate, after preserving the necessary non-sensitive incident evidence.

Checkpoint checksums alone do not establish that a model is free from sensitive-data memorisation.

### Step 7 — Retrain Affected Models When Required

Models trained on compromised dataset versions must not continue to be presented as unaffected.

Where clean replacement models are required, retraining must use an approved, validated dataset version.

Retraining remains subject to project authorisation, compute planning and the applicable milestone and CI requirements.

No automatic retraining should be triggered merely by recording an incident.

### Step 8 — Review Git History Exposure

If a credential was committed to Git:

- Assume the historical value may have been copied.
- Confirm rotation or revocation first.
- Identify affected commits, branches, tags and remote references.
- Evaluate the need for history rewriting.
- Coordinate with affected contributors and repository administrators.
- Assess the effect on signed commits, existing clones and CI evidence.

History rewriting and force-pushing are potentially destructive operations.

**Do not perform a repository history rewrite or force-push without explicit Project Owner authorisation and a verified remediation plan.**

Where a rewrite is approved, follow established repository history-remediation procedures and communicate the need to replace affected clones or references.

History rewriting does not guarantee removal from every fork, cache or external archive.

### Step 9 — Verify Recovery

After remediation:

- Confirm the credential has been revoked or rotated.
- Rerun relevant secret scanning.
- Validate repository artifact protections.
- Test any affected code changes.
- Revalidate dataset provenance where applicable.
- Confirm compromised artifacts are appropriately restricted or retired.
- Obtain required CI evidence for affected changes.
- Record remaining risks and remediation decisions.

An incident is not considered resolved simply because the visible secret no longer appears in `main`.

---

## 07 // Built-In Security Safeguards

KittyLM includes a combination of implemented engineering controls and planned research safeguards.

### 7.1 Current Safeguards

| Safeguard | Relevant component | Status |
|---|---|---|
| Shared secret detection | `kittylm/data/secrets.py` | Implemented |
| Repository secret scanning | `scripts/scan_secrets.py` | Implemented |
| Pre-commit protection | `.githooks/pre-commit` | Implemented |
| Forbidden artifact checks | Repository artifact guard | Implemented |
| CPU-based security CI | `.github/workflows/tests.yml` | Implemented |
| Dependency vulnerability audit | `pip-audit` | Configured |
| Experiment-record security validation | Research ledger | Implemented |
| Checkpoint integrity and restricted loading | Training checkpoint system | Implemented |
| Special-token injection protections | Tokenizer validation | Implemented |
| Generated-sample secret screening | Inference output handling | Implemented |
| Offline end-to-end testing | CPU integration tests | Implemented on tested paths |
| Dataset ingestion security | Future ingestion pipeline | Planned |
| Controlled user-feedback ingestion | Human review and versioning policy | Future integration boundary |

The implementation status describes the presence of the relevant control, not a guarantee of complete security.

### 7.2 Secret Scanner

The shared scanner is defined in:

`kittylm/data/secrets.py`

Findings identify the applicable line and detection rule without storing the matched secret value.

The scanner uses deterministic, auditable detection rules.

It can produce false positives and false negatives.

Unrecognised credential formats may not be detected.

A clean secret scan must not be treated as proof that the repository or dataset contains no sensitive information.

### 7.3 Repository Artifact Guard

Repository checks are intended to prevent accidental commits of prohibited materials, including:

- Credentials and private keys.
- Unauthorised datasets.
- Training checkpoints.
- Model weights.
- Generated samples.
- Local run artifacts.
- Sensitive environment files.

Any approved exception requires documented review and an appropriate release or storage process.

### 7.4 Checkpoint Protections

The current checkpoint system follows architectural decision D-021.

Its implemented design includes:

- A defined checkpoint format.
- Payload integrity checks.
- Restricted deserialisation using `weights_only=True`.
- Validation of expected metadata.
- Compatibility checking.
- Atomic persistence and recovery-oriented file handling.

These protections reduce risks associated with corruption, unsafe loading and accidental incompatibility.

Checksums do not provide authentication against an attacker capable of replacing both an artifact and its checksum.

Do not load arbitrary untrusted checkpoints solely because their file extension or metadata appears valid.

### 7.5 Inference Output Protection

Generated samples are screened before persistence.

Under D-024, flagged lines are replaced with rule-name markers, the resulting text is scanned again, and only approved cleaned output is written.

This reduces the risk of accidentally persisting credential-shaped generated content.

It does not guarantee that a model cannot generate or memorise other sensitive information.

---

## 08 // GitHub Actions & Supply-Chain Security

### 8.1 CI Security

The required workflow is:

`.github/workflows/tests.yml`

The `Test` workflow contains the following jobs:

| Job | Purpose |
|---|---|
| Quality | Source quality and engineering validation |
| Tests — Ubuntu | CPU-based Linux regression tests |
| Tests — Windows | CPU-based Windows regression tests |
| Security | Secret scanning, artifact protection, provenance checks and dependency auditing |

The workflow runs on pushes to `main` and on pull requests according to its configured triggers.

The current workflow defines:

`contents: read`

as its repository token permission baseline.

Workflow action dependencies must be reviewed when changed or upgraded.

### 8.2 Exact-Commit Verification

Under D-018, milestone acceptance requires successful local checks and required GitHub CI on the relevant commit, subject to the documented infrastructure exception.

Formal experiment records have stricter evidence requirements under D-022.

A passing pull-request preview is not equivalent to successful required CI evidence for the exact formal experiment commit.

### 8.3 Dependency Security

Project dependencies should be assessed for:

- Known vulnerabilities.
- Compatibility.
- Licensing.
- Maintenance status.
- Supply-chain integrity.
- Unnecessary privileges or installation behaviour.

Automated dependency updates must not be merged without appropriate review and validation.

A security advisory does not automatically establish that KittyLM is exploitable; its applicability should be investigated and documented.

Likewise, the absence of known advisories does not establish that a dependency is free from vulnerabilities.

### 8.4 Hosted CI and GPU Isolation

Under D-010, KittyLM 0.1 does not operate a self-hosted GitHub Actions GPU runner.

GPU-specific tests run locally on approved development hardware.

This decision avoids exposing personal research machines to arbitrary CI workflow execution.

Any future self-hosted infrastructure would require a separate security architecture and explicit approval.

---

## 09 // Dataset Security & Contamination Response

Dataset processing introduces risks beyond conventional repository security.

These include accidental disclosure, unauthorised collection, training-data poisoning, integrity compromise and evaluation contamination.

### 9.1 Current Development Boundary

The curated `local-v1` corpus and full dataset ingestion pipeline are planned for Milestone F.

No completed formal training dataset is established by the current repository documentation.

Therefore, protections that depend on that pipeline must not be described as operational merely because their design has been approved.

### 9.2 Source Acceptance

Candidate training sources require review of:

- Provenance.
- Licensing and permissions.
- Integrity.
- Privacy and sensitive content.
- Research relevance.
- Applicable processing restrictions.

The future dataset recipe's `allowed_licenses` configuration must gate ingestion.

Public availability alone does not grant unrestricted permission to train on material.

### 9.3 Document Rejection

Under D-006, a source document producing a secret-scan finding must be dropped in full.

Exclusion records must not contain matched secret values.

### 9.4 Dataset Version Integrity

If a source is removed or a processing recipe changes, affected dataset identities must be updated through the approved versioning system.

Previously generated research records must remain traceable to the dataset version actually used.

Contaminated datasets must not be silently replaced under an unchanged identity.

### 9.5 Data Poisoning and Evaluation Contamination

Potential incidents include:

- Deliberately manipulated training examples.
- Malicious control-token sequences.
- Unapproved source substitutions.
- Undocumented duplicate material.
- Leakage between training and evaluation partitions.
- Tampered dataset manifests.
- Unauthorised modification of accepted data.

Responses should preserve evidence, identify affected versions and determine whether experiments remain scientifically valid.

For the complete source governance policy, see [DATA_SOURCES.md](DATA_SOURCES.md).

---

## 10 // Model Security & Responsible Research

KittyLM's current model architecture is experimental.

The project does not claim production-grade assistant security, comprehensive content safety or general-purpose model reliability.

### 10.1 Relevant Threats

Research-relevant model security concerns include:

- Special-token injection.
- Unsafe or incorrect generated code.
- Sensitive-data memorisation.
- Checkpoint manipulation.
- Invalid or malicious input handling.
- Evaluation data leakage.
- Inference resource exhaustion.
- Unauthorised tool execution through future integrations.

### 10.2 Tokenizer Security

The tokenizer follows D-019, which prevents ordinary raw text from being interpreted as reserved special-token identifiers unless explicitly authorised by the caller.

Tokenization and control-token boundaries must remain protected during future changes.

### 10.3 Tool and Agent Integration

KittyLM 0.1 is not authorised to execute arbitrary operating-system operations through model generation.

Future tool-use functionality must be designed behind explicitly reviewed integration boundaries.

Model output must not itself be treated as trusted authorization.

External actions should require appropriate validation, permissions and human or policy-based approval.

### 10.4 Model Quality Limitations

Model-generated statements and code may be incorrect, insecure or misleading.

A model-security report should identify the relevant reproducible behaviour and security impact where possible.

Responsible-use guidance is maintained separately in:

[docs/responsible-use.md](docs/responsible-use.md)

---

## 11 // Secure Research Artifacts & Publication

Research artifacts may contain information about experimental environments, dataset composition, checkpoints or model behaviour.

Their release must be treated as a controlled process.

### 11.1 Protected Artifacts

The following are not ordinarily committed to the source repository:

- Raw or processed training corpora.
- Tokenised dataset files.
- Private manifests or restricted data.
- Model checkpoint payloads.
- Model weights.
- Generated samples.
- Run logs and local caches.
- Files containing credentials or personal information.

### 11.2 Experiment Records

Research records should contain only the data necessary for scientific reproducibility and auditability.

Sensitive environment details must not be included merely for convenience.

Results affected by a security incident must be documented accurately.

A formal result must not be presented as uncompromised when material contamination or tampering is known.

### 11.3 Public Model Releases

Any future public model release requires specific approval.

Review should include:

- Model artifact integrity.
- Appropriate licences.
- Training data provenance.
- Known safety limitations.
- Possible sensitive-data exposure.
- Release documentation.
- Relevant research evidence.

An internal benchmark or successful training run does not automatically authorise public model distribution.

---

## 12 // Coordinated Disclosure

KittyLM encourages responsible vulnerability research and coordinated communication.

### 12.1 Reporter Expectations

Security researchers are asked to:

- Act in good faith.
- Avoid accessing unrelated private information.
- Avoid destructive testing.
- Avoid unnecessary service disruption.
- Use synthetic data wherever practical.
- Test only systems they own or are authorised to assess.
- Avoid publishing exploit details before reasonable coordination.
- Stop testing if unexpected sensitive data or access is encountered.

This policy does not grant permission to attack third-party systems, contributor machines or unrelated infrastructure.

### 12.2 Maintainer Responsibilities

The project maintainer should, where reasonably practicable:

- Review reports fairly.
- Protect sensitive evidence.
- Communicate relevant findings.
- Consider responsible credit for the reporter.
- Avoid unnecessary disclosure.
- Test remediation before announcing resolution.
- Explain important unresolved limitations.

### 12.3 Public Disclosure

Publication timing should consider:

- The severity of the issue.
- Whether active exploitation is known.
- Whether mitigations are available.
- The exposure of sensitive information.
- Potential impact on users or contributors.
- The reporter's legitimate interests.

Public advisories may describe the vulnerability, affected versions, mitigations and relevant evidence without reproducing credentials or private material.

Credit may be provided with the reporter's agreement.

---

## 13 // Security Governance & Accountability

KittyLM is a human-directed research project.

Security-sensitive operations require appropriate authority and documented decisions.

### 13.1 Project Owner Responsibilities

The Project Owner retains final authority over:

- Security policy changes.
- Repository access and administrative permissions.
- Deployment decisions.
- Dataset containment and exclusion approvals.
- Model artifact publication or withdrawal.
- Destructive remediation operations.
- Repository history rewriting.
- Major security architecture changes.

Immediate credential revocation should not be delayed unnecessarily when performed by the credential's authorised owner.

### 13.2 Discrepancy Management

Security findings affecting approved decisions or project assumptions should be recorded in:

[docs/discrepancies.md](docs/discrepancies.md)

Significant architecture changes should also be documented in:

[docs/decisions.md](docs/decisions.md)

Unresolved security issues must not be silently represented as closed.

### 13.3 AI-Assisted Security Work

AI development tools may assist with:

- Static code review.
- Vulnerability analysis.
- Threat modelling.
- Security test planning.
- Incident documentation.
- Mitigation proposals.

Their outputs must be reviewed and validated.

AI assistants must not independently rotate credentials, destroy checkpoints, rewrite Git history, publish advisories or change infrastructure permissions without appropriate authorisation.

A generated security assessment is not a substitute for verified evidence.

---

## 14 // Known Limitations & Security Posture

The following limitations should be considered when evaluating KittyLM's security posture.

**Secret scanning is incomplete by nature.**  
Undetected credential formats and false negatives remain possible.

**Dataset protections are partly planned.**  
The complete source ingestion and provenance pipeline remains a future milestone.

**Checkpoint checksums are not cryptographic authentication.**  
An attacker who can replace both metadata and payload may defeat simple integrity checks.

**CI coverage is environment-specific.**  
Hosted workflows do not replace local GPU validation or comprehensive production security testing.

**Model output screening is limited.**  
Credential-shaped text checks do not provide a complete guarantee against sensitive-data disclosure or harmful model behaviour.

**Offline tests are scoped.**  
The existing end-to-end tests block network access on tested execution paths, but do not establish that every possible future code path is network-free.

**Security settings may change.**  
Repository hosting features such as GitHub private vulnerability reporting, secret scanning and push protection require periodic verification. Previously recorded settings should not be treated as permanently current.

Security claims should always distinguish between implemented protections, tested behaviours, known limitations and future plans.

See [docs/safety.md](docs/safety.md) for the detailed security properties and their implementation status.

---

## 15 // Related Security Documentation

| Document | Purpose |
|---|---|
| [README.md](README.md) | Project architecture and development overview |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Engineering, testing and research requirements |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community conduct and reporting |
| [DATA_SOURCES.md](DATA_SOURCES.md) | Dataset acceptance, provenance and exclusions |
| [docs/safety.md](docs/safety.md) | Security properties and implementation status |
| [docs/responsible-use.md](docs/responsible-use.md) | Responsible AI research and model use |
| [docs/limitations.md](docs/limitations.md) | Known model and engineering limitations |
| [docs/decisions.md](docs/decisions.md) | Architectural and security decisions |
| [docs/discrepancies.md](docs/discrepancies.md) | Open issues and documented resolutions |
| [docs/public-release.md](docs/public-release.md) | Repository publication security checklist |

---

## 16 // Final Security Commitment

KittyLM aims to make scientific experimentation, software engineering and responsible AI development compatible with clear security practices.

We recognise that security is not a permanent state achieved through a single scan, test or policy.

It requires continual review, appropriate controls, responsible handling of incidents and honest communication about remaining risks.

Our security priorities are:

**Protect sensitive information. Preserve research integrity. Validate engineering changes. Respond responsibly to vulnerabilities.**

### `KITTYLM // SECURITY BY DESIGN. RESEARCH WITH INTEGRITY.`

*Protecting the research, the infrastructure and the people behind it.*

**Security contact:** `security@krazykitty.dev`

**© 2026 KrazyKitty — KittyLM Research & Development**
