## KittyLM // Data Sources

**Dataset Provenance · Licensing · Scientific Reproducibility · Privacy · Research Integrity**

**Document:** `DATA_SOURCES.md`  
**Project:** KittyLM — Independent Language Model Research & Development  
**Project Owner:** KrazyKitty  
**Document Version:** 1.0  
**Last Updated:** 10 October 2026  
**Dataset Development Stage:** Pre-ingestion / Milestone F planned

---

> **DATA//STATUS: NO APPROVED TRAINING DATASET**
>
> **No dataset has been built yet.**
>
> KittyLM's curated `local-v1` training corpus and production dataset ingestion pipeline remain planned work under Milestone F.
>
> No dataset listed or discussed as a future candidate should be considered accepted, authorised for ingestion, or approved for model training until it has completed the required provenance, licensing, security and scientific review.

## 01 // Current state

KittyLM is an independent language model research project designed to investigate the development of original autoregressive language models using carefully controlled datasets, reproducible training methodologies and transparent evaluation.

Training data is a fundamental research dependency.

The quality, provenance, licensing, structure and composition of a dataset directly influence model behaviour, experimental validity, reproducibility and potential downstream risks.

For this reason, KittyLM treats dataset governance as part of its scientific engineering infrastructure rather than as a secondary administrative process.

### 1.1 Dataset Status

| Component | Current status |
|---|---|
| Primary training corpus | Not built |
| `local-v1` dataset | Planned — Milestone F |
| Dataset ingestion pipeline | Not yet implemented |
| Dataset provenance manifests | None registered |
| Approved external training sources | None recorded |
| Dataset licence validation | Planned for ingestion pipeline |
| Document-level secret scanner | Implemented as an engineering component |
| Dataset filtering and deduplication | Planned |
| Document-level train/validation/test splitting | Approved design, implementation pending |
| Dataset version generation | Planned |
| Generated source registry | Planned |
| Formal baseline training | Pending prerequisite milestones |

This table reflects the verified repository state at the time of this document revision. It must be updated when new implementation or validation evidence becomes available.

### 1.2 Engineering Fixtures vs Research Datasets

KittyLM contains small engineering fixtures used for testing tokenisation, model execution, training routines and evaluation behaviour.

These fixtures must not be confused with a formally accepted research corpus.

**Engineering fixtures** are designed to prove specific software functions.

**Research datasets** are curated and versioned collections used to investigate language modelling behaviour and performance.

A successful engineering smoke test does not establish dataset quality or general language-model capability.

Under D-017, engineering smoke runs must remain separate from formal research experiments.

### 1.3 Dataset Development Sequence

The approved model-first development strategy (D-015) places dataset pipeline implementation after the GPU engineering validation milestone.

```text
KITTYLM // DATA DEVELOPMENT

      Source Identification
                |
                v
      Licensing & Permission Review
                |
                v
      Privacy & Security Assessment
                |
                v
      Source Approval
                |
                v
      Controlled Data Acquisition
                |
                v
      Document Validation & Filtering
                |
                v
      Deduplication & Integrity Checks
                |
                v
      Deterministic Dataset Splitting
                |
                v
      Tokenisation
                |
                v
      Dataset Version & Provenance Manifest
                |
                v
      Validated Source Registry
                |
                v
      Authorised Research Experiments
```

This diagram describes the intended Milestone F workflow. It does not imply that every stage has already been implemented.

Dataset ingestion and training may proceed only within approved milestone boundaries.

---

## 02 // Source acceptance requirements

KittyLM does not accept training sources solely because they are publicly accessible, technically downloadable or commonly used in machine learning research.

Every proposed source must undergo a documented acceptance process.

### 2.1 Minimum Acceptance Criteria

A candidate source must satisfy the following requirements.

**01 — Identifiable Origin**

The original source must be identifiable and reasonably traceable.

Record its publisher, maintainer, repository, dataset identifier or other appropriate origin.

**02 — Permitted Research Use**

The applicable licence and terms must permit the intended research activities.

Where permissions are unclear, ingestion must be deferred pending review.

**03 — Authenticity & Integrity**

The source must be obtained through an identifiable acquisition process, with appropriate integrity and version information.

**04 — Data Security**

The material must satisfy KittyLM's applicable security controls before acceptance into persistent dataset artifacts.

**05 — Privacy Assessment**

Sources containing personal, confidential or otherwise sensitive information require appropriate review.

Public accessibility alone does not establish permission to use personal information for model training.

**06 — Research Relevance**

The source should contribute meaningfully to the approved dataset objectives, such as language modelling, programming, technical documentation or computer-science research.

**07 — Reproducibility**

The accepted material and processing procedure must be sufficiently documented to support controlled reproduction, subject to applicable distribution restrictions.

**08 — Project Approval**

The Project Owner must approve the source for the relevant dataset version or experiment.

Approval for one research purpose does not automatically grant permission for unrelated uses or future dataset expansions.

### 2.2 Candidate Source Categories

The following categories may be considered during future dataset development.

They are **research candidates, not currently approved source inventories**.

| Category | Potential research purpose |
|---|---|
| Permissively licensed source code | Programming language structure and syntax |
| Official technical documentation | Software engineering terminology and explanations |
| Openly licensed educational material | Computer-science and mathematical concepts |
| Appropriately licensed research text | Technical and scientific language |
| Authorised project documentation | Configuration formats, APIs and developer workflows |
| Carefully reviewed public-domain material | General language modelling |
| Approved synthetic research data | Controlled experimental tasks in later dataset versions |

Every candidate remains subject to its own licence, provenance, security and research evaluation.

### 2.3 Source Acceptance Outcomes

Each proposed source should receive a documented disposition:

| Decision | Meaning |
|---|---|
| Approved | All required acceptance conditions are satisfied |
| Pending review | Further evidence or approval is required |
| Restricted | Use is permitted only under specified conditions |
| Rejected | The source does not meet acceptance requirements |
| Withdrawn | A previous approval has been revoked or superseded |

These dispositions describe the proposed governance workflow. Their eventual machine-readable representation must follow the approved manifest schema.

No source should be silently treated as approved because it was previously used in another project.

---

## 03 // Licensing and provenance

Licensing and source traceability are mandatory aspects of KittyLM dataset governance.

### 3.1 Licensing Requirements

Every training source must declare its applicable licence or other documented permission basis.

The intended Milestone F dataset recipe includes an `allowed_licenses` policy that will restrict which sources may enter the accepted corpus.

The final allowlist must be approved and implemented before ingestion.

Contributors must not assume that:

- Publicly accessible content is automatically licensed for model training.
- Source-code licensing automatically covers all accompanying documentation and assets.
- A repository licence necessarily covers independently contributed third-party material.
- Research access includes redistribution rights.
- A dataset's availability on a hosting platform establishes unrestricted reuse.
- Permission to train a model automatically permits redistribution of the source material.

Where a source combines multiple licensing conditions, those conditions must be examined individually.

### 3.2 Required Provenance Metadata

Approved source manifests should capture the applicable information from the following categories:

| Field | Purpose |
|---|---|
| Source identifier | Unique identity for the accepted source |
| Source name | Human-readable source title |
| Publisher or maintainer | Responsible organisation or individual |
| Source location | Canonical repository, dataset or publication reference |
| Licence | Applicable licensing designation |
| Licence evidence | Reference supporting the permission assessment |
| Source version | Release, revision, snapshot or commit |
| Acquisition method | Documented retrieval procedure |
| Source integrity hash | Verification of acquired material |
| Processing recipe | Applied filtering and transformation configuration |
| Files examined | Scope of source processing |
| Files accepted/rejected | Dataset inclusion accounting |
| Bytes accepted/rejected | Processing and retention accounting |
| Rejection reasons | Documented causes of exclusion |
| Dataset assignment | Relevant dataset version and partition |
| Restrictions | Relevant use or redistribution limitations |

These are documentation requirements and recommended registry fields, not a claim that every field already exists in the current manifest schema.

The eventual implementation must use the schema approved for Milestone F.

### 3.3 Attribution

Where required by applicable licences, attribution must be preserved in an appropriate form.

Dataset provenance documentation should identify upstream creators or maintainers without unnecessarily exposing personal information.

Third-party acknowledgements must not misrepresent authorship, permissions or licensing.

### 3.4 Licence Changes

If a source's terms change:

1. Identify the affected source and versions.
2. Review the applicable terms and permissions.
3. Record the evidence and relevant dates.
4. Determine whether prior acceptance remains appropriate.
5. Suspend new ingestion when permission is unresolved.
6. Document any required remediation or exclusion.
7. Update affected provenance records through the approved process.

A later licensing change should not silently alter previously recorded dataset identities or experimental results.

---

## 04 // Privacy, secrets, and sensitive data

KittyLM applies a security-first approach to dataset ingestion.

Training data may contain credentials, private information, proprietary material or content that was not intended for machine learning research.

Such content must not be accepted merely because it can be accessed.

### 4.1 Secret Detection

The repository includes a secret scanner intended to identify sensitive credential-like material.

Under architectural decision D-006:

**A document that produces a secret-scan finding is excluded in its entirety.**

Partial redaction is not an acceptable substitute for the approved document-level exclusion policy during corpus ingestion.

Only the document identifier and relevant detection rule may be recorded for the exclusion.

The detected secret value must not be retained in the exclusion record.

The ingestion implementation must ensure that required validation takes place before unapproved document contents are written into persistent dataset artifacts, in accordance with D-006.

### 4.2 Sensitive Content Categories

Sources require particular scrutiny when they contain:

- Authentication credentials or access tokens
- Private cryptographic keys
- Passwords or connection strings
- Confidential project files
- Internal organisational documents
- Private correspondence
- Personal contact information
- Financial or medical information
- Sensitive personal records
- Material obtained through unauthorised access
- Proprietary or restricted data without permission

This is not an exhaustive classification.

A source may be inappropriate for training even when an automated secret scanner does not detect anything.

### 4.3 Privacy Review

Privacy review should consider:

- Whether personal information is present.
- Whether the proposed processing has a suitable legal and permission basis.
- Whether the data is necessary for the research objective.
- Whether the material can be excluded or minimised.
- Whether consent or other relevant restrictions apply.
- Whether publication of resulting artifacts creates additional risks.

Contributors must not assume that removing names or email addresses guarantees anonymity.

If personal-data permissions or obligations cannot be established, the source must remain excluded from the accepted corpus until resolved.

### 4.4 No Automatic Training on Feedback

Under decision D-009, KittyLM must not automatically train on user interactions, feedback, chat messages, issue discussions or other unreviewed material.

Any proposed feedback-derived data must pass human review and become part of an explicitly approved, versioned dataset before training.

The existence of a future integration or agent interface does not authorise continuous learning.

### 4.5 Incident Handling

If unauthorised sensitive data is discovered:

1. Stop the affected ingestion or publication workflow.
2. Prevent further exposure.
3. Record the incident without reproducing secret values.
4. Determine which artifacts and systems may be affected.
5. Follow the applicable security reporting and remediation procedures.
6. Revoke or rotate exposed credentials where appropriate and authorised.
7. Rebuild or invalidate affected datasets when necessary.
8. Review whether any downstream checkpoints or outputs require additional handling.

Security concerns should be reported according to [SECURITY.md](SECURITY.md).

Dataset exclusions should not expose the sensitive values that caused rejection.

---

## 05 // Integrity and versioning

A reliable research dataset must have a stable, identifiable relationship to its source material and processing configuration.

### 5.1 Dataset Identity

Each accepted dataset version should be derived from its approved inputs and processing rules.

Relevant identity information includes:

- Source revisions
- Source integrity hashes
- Accepted document identifiers
- Filtering rules
- Deduplication policy
- Dataset partitioning policy
- Processing recipe version
- Relevant pipeline configuration

The exact dataset version derivation procedure must be defined and tested during Milestone F.

Do not invent or manually assign content hashes that have not been calculated.

### 5.2 Document Deduplication

The initial dataset pipeline is expected to include deterministic duplicate handling.

Exact duplicate detection helps reduce repeated material and potential contamination across data partitions.

Near-duplicate detection may be introduced in a later approved revision.

Until such functionality is implemented and evaluated, do not describe the dataset as comprehensively deduplicated.

### 5.3 Train, Validation and Test Separation

Under D-005, KittyLM's approved initial design uses deterministic document-level content-hash buckets.

The intended dataset proportions are:

| Partition | Allocation |
|---|---:|
| Training | 98% |
| Validation | 1% |
| Test | 1% |

These are target bucket allocations, not guaranteed exact realised percentages for every corpus.

Splitting at the document level is intended to reduce leakage caused by placing windows or chunks from the same document in multiple partitions.

The pipeline must preserve deterministic assignments and provide validation evidence.

Related documents, forks, duplicated content and near duplicates may still create leakage risks, requiring additional analysis.

### 5.4 Tokenisation and Dataset Compatibility

The tokenised dataset must remain traceable to the tokenizer configuration used to construct it.

The primary research vocabulary is planned at 16,384 tokens, with approved controlled vocabulary-size comparisons.

Tokenizer artifacts, special-token mappings and dataset versions must be recorded accurately.

Changing tokenization or dataset processing parameters must not silently reuse the identity of an incompatible earlier dataset.

### 5.5 Integrity Validation

The eventual pipeline should validate:

- Source identity and approved provenance
- Applicable licence status
- Input integrity where reference hashes are available
- Document processing and exclusion accounting
- Deterministic partitioning
- Output manifest consistency
- Dataset version reproducibility
- Tokenizer compatibility
- Absence of forbidden committed artifacts

Validation failures must be reported explicitly.

They must not be bypassed merely to produce an apparently complete dataset build.

### 5.6 Research Artifact Boundaries

Raw, cleaned and tokenised datasets must not be committed to the ordinary source repository under the current artifact policy.

Likewise, private corpus material and unapproved training outputs must remain outside tracked source artifacts.

Dataset manifests may be committed only when they comply with the project's privacy, security, licensing and provenance requirements.

Manifests should use appropriate relative references rather than disclose local usernames, hostnames or absolute filesystem paths.

---

## 06 // Future generated registry

`DATA_SOURCES.md` is intended to become a deterministic, validated dataset provenance registry when the Milestone F tooling is implemented.

At present, the dataset registry generator has not been established.

The existing provenance check verifies the no-dataset statement while rejecting unvalidated dataset recipes or manifests.

### 6.1 Planned Registry Behaviour

Once implemented, the generator should derive accepted-source information from validated dataset manifests.

Expected properties include:

- Deterministic output
- Consistent source ordering
- Versioned provenance references
- Explicit licence information
- Accepted and rejected source accounting
- No embedded secret values
- No private absolute filesystem paths
- No volatile generation timestamps that break reproducibility
- CI detection of unexpected differences between generated and committed output

The precise generated format must be defined in the approved Milestone F implementation.

### 6.2 Current Source Registry

**No dataset has been built yet.**

| Source ID | Source name | Licence | Dataset version | Status |
|---|---|---|---|---|
| — | No approved dataset sources registered | — | — | Not available |

This table is a current-state placeholder, not a generated manifest listing.

It must not be populated with proposed sources until acceptance records exist.

### 6.3 Generated Registry Fields

A future approved source table may include:

| Field | Description |
|---|---|
| Source ID | Stable accepted-source identifier |
| Source | Human-readable title |
| Licence | Verified applicable licence |
| Revision | Source snapshot or version |
| Files kept | Accepted file count |
| Files dropped | Rejected file count |
| Bytes kept | Accepted byte count |
| Bytes dropped | Excluded byte count |
| Drop reasons | Validated exclusion categories |
| Dataset | Version containing the accepted material |

These columns are a proposed presentation format, not a replacement for the manifest schema.

### 6.4 Generated File Integrity

Once generator-based source tracking is active:

**Do not manually edit generated source entries or measured dataset statistics.**

Changes to source records must originate from validated manifests and authorised pipeline operations.

This document's static governance sections must also remain synchronised with the generator.

The Milestone F implementation should either preserve the approved static text while regenerating the registry or formally separate governance documentation from generated provenance output.

The choice must be made before activating full generated-file consistency checks.

### 6.5 Dataset Publication

A dataset may not be published merely because its registry entry is valid.

External publication additionally requires review of:

- Source licence and redistribution permissions
- Privacy and confidentiality risks
- Data provenance completeness
- Dataset composition and quality limitations
- Security findings
- Documentation accuracy
- Project Owner approval

Source data and trained model weights may have different permission requirements.

A successful internal training run does not automatically authorise dataset redistribution.

---

## 07 // Excluded sources

KittyLM maintains explicit exclusion principles to protect research integrity, licensing compliance, privacy and security.

### 7.1 Sources Ineligible for Acceptance

Material must be excluded from the accepted corpus when it falls into a prohibited category or fails mandatory review requirements.

| Exclusion category | Reason |
|---|---|
| Unknown or unresolved permissions | Research use has not been authorised |
| Licence-incompatible material | Source conditions conflict with the intended use |
| Unauthorised private repositories | Confidentiality and access restrictions |
| Leaked credentials or secret-bearing documents | Security exposure |
| Unauthorised personal information | Privacy and data protection |
| Unlawfully obtained material | Unacceptable provenance |
| Proprietary content without adequate rights | Intellectual property restrictions |
| Tampered or unverifiable material | Integrity and reproducibility concerns |
| Unreviewed user conversations or feedback | Violates human-reviewed feedback policy |
| Unapproved external dataset downloads | Outside accepted dataset scope |
| Documents failing required security validation | Must be rejected under the applicable security rules |

A detected issue may affect individual documents or the eligibility of the entire source, depending on its nature.

For secret-scan findings, D-006 requires rejection of each flagged document in full.

### 7.2 Deferred Research Sources

Some source categories may be scientifically useful but remain outside KittyLM's currently approved scope.

Examples include:

- Large external pretraining corpora
- Third-party language model datasets
- Community-curated programming corpora
- Automatically harvested website content
- Synthetic instruction datasets
- AI-generated dialogue corpora
- Specialist security research collections
- Feedback-derived training datasets

These are not permanently prohibited simply because they are deferred.

They require relevant source review, technical planning and approval before ingestion.

### 7.3 Synthetic Data Policy

Under D-016, synthetic data generators are deferred from `local-v1` to a proposed `local-v2` research stage after the initial baseline experiment.

`local-v1` must not silently incorporate synthetic training material contrary to the approved scope.

Future synthetic data should have documented generator versions, seeds, construction methods and quality controls.

Synthetic data is not automatically free of privacy, licensing or research-contamination risks.

### 7.4 External Research Collaborations

Datasets developed by other independent researchers or collaborative projects are not automatically KittyLM assets.

A collaborator's permission to discuss, inspect or evaluate a dataset does not imply permission to ingest, train on or redistribute its contents.

Any external research material must follow the same acceptance process as other third-party sources.

Collaborative arrangements should establish applicable permissions and attribution before material enters the accepted corpus.

### 7.5 Exclusion Records

When the dataset pipeline is implemented, exclusion accounting should be recorded without exposing sensitive content.

Depending on the applicable schema, records should capture:

- Safe document or source identifier
- Relevant exclusion rule
- Processing stage
- Applicable source version
- Non-sensitive counts and measurements

Sensitive matching values must not be written into exclusion logs.

### 7.6 Current Exclusion Registry

No completed dataset ingestion or exclusion accounting has been recorded in the current repository snapshot.

Therefore:

**No source-level rejection counts or exclusion statistics are available.**

This does not establish that any future candidate source is acceptable.

It means that the approved dataset ingestion workflow has not yet produced validated results.

---

### DATA//GOVERNANCE — Final Statement

KittyLM's data governance exists to make research reliable, auditable and responsible.

Training data is not simply input for a model. It is part of the experiment itself.

Every accepted source influences the scientific interpretation of the resulting model, and every undocumented processing decision weakens the reproducibility of that research.

The project's objective is to build datasets that can be meaningfully inspected, evaluated and traced back to their origins.

**Our commitments:**

- Provenance before ingestion.
- Permission before use.
- Security before persistence.
- Integrity before tokenisation.
- Reproducibility before experimentation.
- Evidence before publication.

### `KITTYLM // DATA INTEGRITY IS RESEARCH INTEGRITY.`

*Curated with care. Validated through evidence. Developed responsibly.*

**© 2026 KrazyKitty — KittyLM Research & Development**
