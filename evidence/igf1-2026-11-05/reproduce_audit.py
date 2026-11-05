"""Read-only IGF1 source audit; Python standard library only.

Inputs are the public OpenGenes SQLite snapshot and Europe PMC's supplementary
ZIP for PMC4326899. Results are written to a separate output directory.
"""

import argparse
import collections
import csv
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import statistics
import xml.etree.ElementTree as ET
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--supplements", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() in {args.database.resolve(), args.supplements.resolve()}:
        parser.error("Output must be a separate directory, not an input file")
    args.output.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.supplements) as archive:
        data = archive.read("acel0013-0408-sd1.docx")
    with zipfile.ZipFile(io.BytesIO(data)) as document:
        root = ET.fromstring(document.read("word/document.xml"))
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    table = root.find(".//w:tbl", ns)
    groups = collections.defaultdict(list)
    records, date_conflicts, dates_not_evaluated = [], [], []
    cage = genotype = sex = None
    for row_number, row in enumerate(table.findall("w:tr", ns)[1:], start=2):
        cells = ["\n".join("".join(t.text or "" for t in p.findall(".//w:t", ns))
                           for p in cell.findall("w:p", ns)).strip()
                 for cell in row.findall("w:tc", ns)]
        if len(cells) != 8:
            raise ValueError(f"Unexpected Table S1 row structure: {row_number}")
        cage, genotype, sex = cells[0] or cage, cells[2] or genotype, cells[3] or sex
        record = dict(source_table_row=row_number, cage=cage, mouse=cells[1],
                      genotype=genotype, sex=sex, dob=cells[4], dod=cells[5],
                      reported_age_days=int(cells[6]), reported_summary=cells[7])
        records.append(record)
        groups[(genotype, sex)].append(record["reported_age_days"])
        if not cells[4] or not cells[5]:
            dates_not_evaluated.append({"source_table_row": row_number, "reason": "DOB or DOD not explicitly repeated; merged date cells not inferred"})
            continue
        try:
            days = (datetime.strptime(cells[5], "%m/%d/%y") - datetime.strptime(cells[4], "%m/%d/%y")).days
            if abs(days - record["reported_age_days"]) > 1:
                date_conflicts.append({**record, "computed_date_difference_days": days})
        except ValueError as error:
            dates_not_evaluated.append({"source_table_row": row_number, "date_parse_error": str(error)})

    with (args.output / "table-s1-transcription.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    connection = sqlite3.connect(args.database.resolve().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        db_records = [dict(row) for row in connection.execute(
            "SELECT rowid AS snapshot_rowid, * FROM lifespan_change WHERE doi = ?",
            ("10.1111/acel.12188",),
        )]
    finally:
        connection.close()
    result = dict(
        database_sha256=hashlib.sha256(args.database.read_bytes()).hexdigest(),
        supplement_docx_sha256=hashlib.sha256(data).hexdigest(),
        listed_animal_rows=len(records),
        descriptive_checks_not_survival_reanalysis=[
            dict(genotype=k[0], sex=k[1], n=len(a), mean_days=statistics.mean(a),
                 median_days=statistics.median(a), min_days=min(a), max_days=max(a))
            for k, a in groups.items()
        ],
        date_conflicts=date_conflicts, dates_not_evaluated=dates_not_evaluated,
        snapshot_records=db_records,
        warning="Descriptive checks only; no date repair, censoring model, clinical inference, or data correction. Merged group cells are carried forward. Native DOCX rendering was not performed.",
    )
    (args.output / "audit.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} source rows and {len(db_records)} snapshot records")


if __name__ == "__main__":
    main()
