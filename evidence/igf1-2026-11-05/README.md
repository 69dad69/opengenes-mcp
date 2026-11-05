# IGF1 liver intervention evidence review

Prepared 5 November 2026. This review supports a reference-QA correction and a curator investigation; it does not authorize a database migration. Confidence is high for the cohort-provenance conflict and the loss of significance information in the reference QA. Numeric source corrections remain unresolved.

## Primary source and cohort separation

Gong et al., Aging Cell 2014, DOI [10.1111/acel.12188](https://doi.org/10.1111/acel.12188), PMID [24341939](https://pubmed.ncbi.nlm.nih.gov/24341939/), PMCID [PMC4326899](https://pmc.ncbi.nlm.nih.gov/articles/PMC4326899/). Read at the publisher and in Europe PMC XML. Attribution: Gong and coauthors, 2014; article and supplement distributed under CC BY 3.0 as recorded in the article XML.

| Experiment | Organism and background | Intervention and timing | Control / intervention n | Outcome and source locator |
|---|---|---|---|---|
| Congenital LID, male | Mouse; mixed C57BL/6, FVB/N, 129sv | Liver albumin-promoter Cre; early postnatal recombination | Figure 1: 15 / 16 | Shorter survival, log-rank P=.006; Results, Figure 1 |
| Congenital LID, female | Mouse; mixed background | Same LID model | Figure 1: 25 / 17 | Survival difference not significant; Figure 1 |
| Inducible iLID, male | Mouse; C57BL/6 | Liver inducible Cre; tamoxifen at one year; controls also treated | Endpoint-specific groups | Pathology and health measurements at two years; no survival study; Introduction, Results and Methods |

Thus, survival values must not be attributed to the adult-induced experiment. The findings concern mice, not human rejuvenation. Additional source details must be checked before translating interventions across studies.

## Snapshot records

Fresh download on 5 November 2026 has SHA-256 `1d34bedfbdc544627b4e0b14c88134e098318d163d1a943343ec6da9bc8ca0b1`, unchanged from 26 October. The database was opened in SQLite read-only mode. Exact extracted records and SQL are in `database-evidence.json`.

| Snapshot record | Control / experiment n | Median / maximum changes | Significance flags, median / maximum | Stored intervention metadata |
|---|---|---|---|---|
| IGF1, mouse, male, DOI 10.1111/acel.12188 | 15 / 16 | -27.5% / -10.8% | 1 / 1 | combined (inducible mutation); tamoxifen |
| IGF1, mouse, female, same DOI | 25 / 17 | +2.9% / +3.9% | 0 / 0 | combined (inducible mutation); tamoxifen |

The n values identify the Figure 1 cohorts, while the drug/induction metadata describe a different experiment. Do not use SQLite rowid as a durable scientific identifier; use DOI, gene, organism, sex and cohort sizes, plus the snapshot hash. Snapshot-local rowids are retained only for reproducibility.

The database's `HGNC` column stores the human gene symbol IGF1. Official HGNC lookup returned HGNC:5464, NCBI Gene 3479, Ensembl ENSG00000017427. These identify the human gene label; the experimental organism is mouse. They must not be treated as mouse accession numbers. Authority: [HGNC REST](https://rest.genenames.org/fetch/symbol/IGF1).

## Supporting Table S1 audit

Downloaded from [Europe PMC supplementary files](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4326899/supplementaryFiles). Source archive member: `acel0013-0408-sd1.docx`, 209843 bytes, SHA-256 `0b141642c8abb4ed2ec5a8767a7ed1b5d0fc7d69a459d3ec4d2243c23c0d74d9`. The publisher calls it `acel12188-sup-0001-MethodsS1-TableS1-S6.docx`.

The first table contains 74 animal rows. Its summary header specifies Mean +/- SEM. OOXML visible text was extracted with merged cage/genotype/sex values carried forward; EndNote field instructions were excluded. Dates missing from continuation cells were not inferred and are listed separately as not evaluated, rather than as date conflicts. `table-s1-transcription.csv` preserves the observations and `table-s1-audit.json` records checks and limitations.

| Group | Listed animal rows | Arithmetic mean of listed Age days | Median of listed Age days |
|---|---:|---:|---:|
| Male control | 16 | 1013.5625 | 1036 |
| Male LID | 16 | 835.5625 | 793 |
| Female control | 25 | 1042.76 | 1022 |
| Female LID | 17 | 1086.764706 | 1082 |

These are descriptive calculations from the listed age field, not survival-model estimates. The male control count differs from Figure 1's 15. Cage 10 mouse 1 has DOB 04/27/02 and DOD 05/04/01, inconsistent with reported age 738 days. Dates were not silently repaired. Article prose, summary day/month values and exported statistics cannot be automatically reconciled. No censoring assumptions, unit-conversion corrections, numerical replacements or p-value recalculations are proposed.

The bundled renderer was attempted but failed because LibreOffice was absent. The DOCX was inspected structurally, not visually; no edited DOCX is delivered. Source anomalies should be confirmed in a visual review before contacting authors about possible publication errors.

## Other positive liver record

The current QA query also returns a female IGF1 record for DOI [10.1007/s11357-017-9971-0](https://doi.org/10.1007/s11357-017-9971-0), PMID [28409331](https://pubmed.ncbi.nlm.nih.gov/28409331/). The snapshot reports median +16.1% with flag 1, maximum +2.5% with flag NULL, and no mean change. The revised reference labels these as database-reported values, preserving NULL as unreported.

The publication identity and publisher abstract were checked. Its exact cohort, endpoint calculations, and significance flags were not independently validated against full text. Europe PMC's fullTextXML endpoint returned HTTP 500 twice. This record prevents replacing the reference answer with an unqualified negative; it does not validate every stored field. The [publisher abstract](https://link.springer.com/article/10.1007/s11357-017-9971-0) also cautions that late-life IGF1 deficiency did not increase lifespan.

## Export provenance and remaining ownership question

The freshly downloaded [Hugging Face file](https://huggingface.co/datasets/longevity-genie/bio-mcp-data/blob/main/opengenes/open_genes.sqlite) is byte-identical to [open-genes/longevity-gpts open_genes/data/open_genes.sqlite](https://github.com/open-genes/longevity-gpts/blob/main/open_genes/data/open_genes.sqlite). GitHub history for the latter path lists commit `c7a4a0876c522f66a566b272715bc6e8bc3f215a` dated 16 September 2024 as the most recent path commit returned. Byte identity supports a shared exported artifact, not proof of which person or transformation introduced the metadata error.

The current frontend's [download page](https://github.com/open-genes/open-genes-frontend/blob/develop/src/app/pages/download/download-page.component.ts) calls `generatePurpleTable`; the [CSV service](https://github.com/open-genes/open-genes-frontend/blob/develop/src/app/core/services/csv-export-service.ts) obtains `/api/research/lifespan-change` and maps intervention metadata into TSV. The legacy [TSV importer](https://github.com/open-genes/longevity-gpts/blob/main/preprocessing/add_tsv_to_db.py) imports columns into SQLite. The historical original TSV and complete build manifest were not located. These paths suggest a source/export correction followed by re-export, rather than a hardcoded SQLite override.

A single live request to `https://open-genes.com/api/gene/IGF1` timed out after 20 seconds. No current source CMS row IDs were obtained. This is an access limitation, not evidence that the production API is broken.

## Prepared contribution and next action

The separate `fix/liver-lifespan-reference` branch changes `test/test_qa.json` and adds `test/test_liver_reference.py`. It preserves candidate rows while exposing sex, cohort sizes, provenance, mean/median/maximum endpoints and per-endpoint significance. It makes no source-data edits and does not close issue #6.

Before: five focused tests, four failures. After: all five pass. The new SQL also returns the expected two candidates on the downloaded database. The patch applies to a fresh upstream-base archive; diff whitespace checks pass. Full upstream/MCP/LLM tests were not run. See `validation.json` and test logs.

Next curator decision: confirm the original source records and the controlled vocabulary for congenital LID, separate iLID health/pathology data, then regenerate exports. Resolve numerical discrepancies separately with documented estimators and possible censoring/exclusions. The focused code contribution and this evidence review have separate scopes.

Public test logs replace the local workspace path with `<workspace>`; test outcomes are unchanged.
