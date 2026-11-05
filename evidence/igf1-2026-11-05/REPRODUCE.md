# Reproducing the focused checks

Use Python 3.10 or newer. No third-party packages or API keys are required.

## Reference QA regression

Apply `liver-reference.patch` to opengenes-mcp base `02accbdc443200ba1cd755cbb165f57ef5ff5b6d`, then run from the repository root:

```sh
git apply --check /path/to/liver-reference.patch
git apply /path/to/liver-reference.patch
python -m unittest discover -s test -p test_liver_reference.py -v
```

The patch is independent of the earlier publication-count contribution. Its only changed existing QA entry is the liver-intervention question. The `pr-ready` directory provides complete files for inspection; avoid replacing whole files if other contributions have already modified them.

## Source audit

Download these public inputs, preserving their filenames:

- [OpenGenes SQLite](https://huggingface.co/datasets/longevity-genie/bio-mcp-data/resolve/main/opengenes/open_genes.sqlite)
- [Europe PMC supplementary ZIP](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4326899/supplementaryFiles)

Run the supplied read-only audit script, choosing a separate output directory:

```sh
python reproduce_audit.py --database /path/to/open_genes.sqlite --supplements /path/to/igf1-supplements.zip --output /path/to/audit-output
```

Compare the input hashes to `validation.json` before comparing results. For the checked files, expect 74 listed animal rows, four groups (16, 16, 25, 17), and two Gong 2014 database records. The script reads the visible OOXML table and carries merged group cells forward. It flags inconsistent dates without correcting them. Statistics are descriptive summaries of the listed age values, not Kaplan-Meier estimates or a substitute for author/curator review.

The complete native DOCX could not be rendered in this environment because bundled LibreOffice was absent. Open Table S1 visually before using these findings to propose a publication correction. The package includes no modified scientific source data.
