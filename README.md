# OSINT Fusion Engine – Evidence-Backed Exposure Analysis  
### (Proof of Concept)

## Overview

This project is a proof-of-concept OSINT fusion engine that ingests a real, public GitHub commit URL provided via the command line and converts it into evidence-backed claims with explicit uncertainty and exposure risk scoring.

The system prioritizes:
- provenance
- explainability
- ethical restraint

It intentionally avoids identity confirmation or opaque inference.


## Motivation

Public digital platforms expose metadata that can contribute to identity or organizational exposure.  
Most OSINT tools focus on data collection, but fail to clearly explain **why** a conclusion exists.

This project demonstrates how OSINT data can be used to:
- preserve raw artifacts
- extract only observable signals
- model claims probabilistically
- assess exposure rather than assert truth


## Architecture (High Level)
Public Source (GitHub Commit URL)
|
v
RawArtifact (source + timestamp)
|
v
Signal Extraction (username, metadata)
|
v
Claim (probabilistic, not factual)
|
v
Evidence (weighted, inspectable)
|
v
Exposure Risk Score (explainable)

**Key principle:**  
Correlation increases confidence, not proof.


## What the System Does

- Accepts a public GitHub commit URL via CLI input
- Preserves it as a RawArtifact with timestamp and provenance
- Automatically extracts observable metadata such as:
  - author username
  - commit message (if available)
  - commit timestamp (if available)
  - public email (if exposed)
- Models identity assertions as **claims**, not facts
- Supports claims using explicit **evidence**
- Computes an explainable exposure score (0.0–1.0)


## What the System Does NOT Do

- Confirm personal or organizational identity
- Use AI/ML black boxes
- Perform private or authenticated data access
- Scrape behind authentication
- Track individuals

This is **OSINT assessment**, not surveillance.


## Tech Stack

- Python 3
- `requests` – HTTP retrieval
- `beautifulsoup4` – HTML parsing
- Dataclasses – schema enforcement for structure and clarity

No databases or ML models are used to prioritize transparency and auditability.


## Exposure Scoring Logic (Explainable)

Exposure is derived from observable evidence:

| Signal Type               | Weight |
|---------------------------|--------|
| Public commit email       | 0.5    |
| Author username           | 0.2    |
| Commit timestamp          | 0.1    |
| Commit message            | 0.1    |

Scores are capped at **1.0**.

Stronger signals (e.g., email exposure) contribute more than weaker signals (e.g., usernames).


## Limitations

- Single modality (GitHub commits only)
- HTML-dependent extraction (platform changes may affect parsing)
- Manual risk weighting (not statistically calibrated)

These are intentional trade-offs given hackathon constraints.



## Ethical Considerations

- Uses only publicly available data
- Avoids identity confirmation
- Risk scoring reflects exposure, not intent
- Designed to discourage misuse through uncertainty modeling


## Future Extensions

- Multi-commit aggregation
- Image metadata ingestion
- Social media signal correlation
- Graph-based visualization
- Temporal exposure analysis

The architecture supports extension without changing the reasoning layer.


## How to Run

Install dependencies:

pip install requests beautifulsoup4


Run the tool with a public GitHub commit URL

python demo.py https://github.com/<owner>/<repo>/commit/<commit_hash>

Author

Solo hackathon project
Built for learning, transparency, and responsible OSINT practice.