"""Example demonstrating how to read mock candidate profiles from a CSV file

and import them in batch to a Reactive Resume server.
"""

import csv
from io import StringIO

from reactive_resume import RxResumeClient
from reactive_resume.models import Basics, ResumeImportData

# Mock CSV string containing candidates
MOCK_CSV = """name,headline,email,phone,website
Ata Can Yaymacı,Backend Engineer,ata@example.com,+905555555555,https://ata.me
John Doe,Frontend Developer,john@example.com,+1234567890,https://john.me
Alice Smith,AI Architect,alice@example.com,+447777777777,https://alice.me
"""


def parse_candidates_from_csv(csv_data: str) -> list[dict[str, str]]:
    """Parse CSV rows into dictionaries."""
    f = StringIO(csv_data)
    reader = csv.DictReader(f)
    return list(reader)


def bulk_import_candidates(base_url: str, api_key: str, candidates: list[dict[str, str]]) -> None:
    """Iterate through candidates and import them as resumes."""
    # Initialize Sync Client
    with RxResumeClient(base_url=base_url, api_key=api_key) as client:
        print(f"Starting bulk import of {len(candidates)} candidates...")

        for idx, candidate in enumerate(candidates, start=1):
            import_data = ResumeImportData(
                title=f"{candidate['name']} - Profile Resume",
                basics=Basics(
                    name=candidate["name"],
                    headline=candidate["headline"],
                    email=candidate["email"],
                    phone=candidate["phone"],
                    website=candidate["website"],
                ),
            )

            try:
                resume = client.resumes.import_resume(import_data)
                print(f"[{idx}/{len(candidates)}] Imported: {resume.name} (Slug: {resume.slug})")
            except Exception as e:  # noqa: BLE001
                print(f"[{idx}/{len(candidates)}] Failed to import {candidate['name']}: {e}")


if __name__ == "__main__":
    # URL and API Key for server
    SERVER_URL = "https://rxresu.me"
    API_KEY = "your_api_key_here"

    # Execute
    candidate_list = parse_candidates_from_csv(MOCK_CSV)
    bulk_import_candidates(SERVER_URL, API_KEY, candidate_list)
