"""Extract Supplementary Table S1 into a normalized CSV dataset."""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).parent
DEFAULT_PDF = ROOT / "data" / "pone.0274248.s001.pdf"
DEFAULT_CSV = ROOT / "data" / "pone_review_S1_table.csv"
REGIONS = "AFRO|AMRO|EMRO|EURO|SEARO|WPRO"
ROW_PATTERN = re.compile(
    rf"^\s*(?P<study>.+?)[ \t]{{2,}}(?P<sample_size>\d+)[ \t]{{2,}}"
    rf"(?P<infected_cases>\d+)[ \t]{{2,}}(?P<country>.+?)[ \t]{{2,}}"
    rf"(?P<who_region>{REGIONS})[ \t]{{2,}}(?P<year>\d{{4}})\s*$"
)


def pdf_text(pdf_path: Path) -> str:
    """Return layout-preserving PDF text using Poppler's pdftotext."""
    command = shutil.which("pdftotext")
    if command is None:
        raise RuntimeError("pdftotext is required; install Poppler and try again.")
    result = subprocess.run(
        [command, "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def parse_rows(text: str) -> list[dict[str, object]]:
    """Parse rows, excluding table headers and the final aggregate total."""
    rows: list[dict[str, object]] = []
    for line in text.splitlines():
        match = ROW_PATTERN.match(line)
        if match is None:
            continue
        row = match.groupdict()
        sample_size = int(row["sample_size"])
        infected_cases = int(row["infected_cases"])
        year = int(row["year"])
        if not 1900 <= year <= 2100 or not 0 <= infected_cases <= sample_size:
            raise ValueError(f"Invalid table row: {line}")
        rows.append(
            {
                "study": row["study"].strip(),
                "sample_size": sample_size,
                "infected_cases": infected_cases,
                "prevalence": round(infected_cases / sample_size, 8),
                "country": row["country"].strip(),
                "who_region": row["who_region"],
                "year": year,
            }
        )
    if not rows:
        raise ValueError("No study rows were found in the PDF.")
    return rows


def write_csv(rows: list[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--output", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()

    rows = parse_rows(pdf_text(args.pdf))
    write_csv(rows, args.output)
    print(f"Wrote {len(rows)} study records to {args.output}")


if __name__ == "__main__":
    main()
