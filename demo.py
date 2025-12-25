import sys
from datetime import datetime
from extract_commit import extract_commit_details
from schema.raw_artifact import RawArtifact
from schema.account import Account
from schema.claim import Claim
from schema.evidence import Evidence

def extract_commit_hash(commit_url):
    return commit_url.rstrip("/").split("/")[-1]


def calculate_exposure_score(evidence_items):
    score = 0.0

    for ev in evidence_items:
        if ev.method == "commit email":
            score += 0.5
        elif ev.method == "commit author username":
            score += 0.2
        elif ev.method == "commit message":
            score += 0.1
        elif ev.method == "commit timestamp":
            score += 0.1

    return min(score, 1.0)


# STEP 1: Raw data (real GitHub commit page)
if len(sys.argv) < 2:
    print("Usage: python demo.py <github_commit_url>")
    sys.exit(1)

commit_url = sys.argv[1]
commit_hash = extract_commit_hash(commit_url)

artifact = RawArtifact(
    artifact_id="A1",
    artifact_type="webpage",
    source_url=commit_url,
    retrieved_at=datetime.now(),
    stored_path=f"raw/commit_{commit_hash}.html",
    hash=commit_hash
)

# STEP 2: Extracted account
commit_data = extract_commit_details(commit_url)
author_username = commit_data["author"]
author_email = commit_data["email"]
commit_message = commit_data["message"]
commit_time = commit_data["timestamp"]

account = Account(
    account_id="ACC1",
    platform="github",
    username=author_username if author_username else "unknown",
    confidence=1.0 if author_username else 0.5
)

# STEP 3: Claim (NO certainty)
claim = Claim(
    claim_id="CL1",
    claim_type="identity",
    statement=f"GitHub account '{author_username}' exposes identity-related metadata through public commits",
    confidence=0.5 if author_username else 0.3
)

# STEP 4: Evidence
evidence_items = []

if author_username:
    evidence_items.append(Evidence(
        evidence_id="E1",
        artifact_id=artifact.artifact_id,
        method="commit author username",
        weight=0.2,
        notes="Username extracted from commit author field"
    ))

if commit_message:
    evidence_items.append(Evidence(
        evidence_id="E2",
        artifact_id=artifact.artifact_id,
        method="commit message",
        weight=0.1,
        notes=f"Commit message: {commit_message}"
    ))

if commit_time:
    evidence_items.append(Evidence(
        evidence_id="E3",
        artifact_id=artifact.artifact_id,
        method="commit timestamp",
        weight=0.1,
        notes=f"Commit time: {commit_time}"
    ))

if author_email:
    evidence_items.append(Evidence(
        evidence_id="E4",
        artifact_id=artifact.artifact_id,
        method="commit email",
        weight=0.3,
        notes=f"Public email exposed: {author_email}"
    ))
exposure_score = calculate_exposure_score(evidence_items)


print("\n--- OSINT PROTOTYPE OUTPUT ---")
print("RAW ARTIFACT:", artifact)
print("ACCOUNT:", account)
print("CLAIM:", claim)
print("\nEVIDENCE:")
for ev in evidence_items:
    print("-", ev)

print(f"\nEXPOSURE SCORE: {exposure_score}")
