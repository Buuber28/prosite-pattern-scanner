
# PROSITE Pattern Scanner

A small command-line tool for scanning FASTA sequences for PROSITE-style sequence motifs.

The script accepts either a manually provided PROSITE pattern or a PROSITE accession ID. If a PROSITE ID is given, the pattern is downloaded from the PROSITE database, converted into a regular expression, and searched against the input FASTA sequences.

## Features

- Reads FASTA input from a file or standard input
- Supports direct PROSITE-style pattern input
- Can download PROSITE patterns automatically by ID
- Reports overlapping matches
- Outputs sequence ID, 1-based start position, and matched sequence

## Usage

Scan with a manually provided pattern:

```bash
python psscan.py --fasta input.fasta --pattern "N-{P}-[ST]-{P}"
```

Fetch a pattern from PROSITE:

```bash
python psscan.py --fasta input.fasta --web PS00001
```

Read FASTA input from standard input:

```bash
cat input.fasta | python psscan.py --fasta - --pattern "N-{P}-[ST]-{P}"
```

## Output Format

The script prints tab-separated results:

```text
sequence_id    start_position    matched_sequence
```

Example:

```text
protein_1    45    NATS
```

## Arguments

| Argument | Description |
|---|---|
| `--fasta` | Path to a FASTA file, or `-` to read from standard input |
| `--pattern` | PROSITE-style pattern supplied directly |
| `--web` | PROSITE ID used to download the pattern automatically |

`--pattern` and `--web` are mutually exclusive.
