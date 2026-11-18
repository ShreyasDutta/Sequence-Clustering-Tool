# DNA Sequence Clustering Tool (Simple Version)

A beginner-friendly Python project that groups DNA sequences based on percentage similarity.

## Files
- `SequenceClusterTool_Simple.py` — core program: reads FASTA files, calculates GC content and sequence similarity, and groups sequences using a similarity threshold.
- `Simple_App.py` — desktop GUI version using Python's built-in Tkinter library.

## Requirements
- Python 3
- Tkinter (usually included with standard Python installations)

No third-party Python packages are required.

## Run the core program
```bash
python SequenceClusterTool_Simple.py
```

## Run the desktop application
```bash
python Simple_App.py
```

The desktop application opens with sample DNA sequences already loaded. You can edit the FASTA input, change the similarity threshold (default: 80%), and click **Cluster Sequences**.

## FASTA input format
Each sequence starts with a header beginning with `>` followed by one or more lines of DNA sequence.

```text
>Sequence_1
ATGCGTACGTAG
>Sequence_2
ATGCGTACGTAA
```

## How clustering works
1. Read the sequences.
2. Calculate GC content for each sequence.
3. Compare sequences character by character.
4. If a sequence has similarity greater than or equal to the chosen threshold with a cluster's representative sequence, add it to that cluster.
5. Otherwise, start a new cluster.

## Important limitation
This is the simple, educational version. Its similarity calculation compares characters at matching positions and does not perform sequence alignment or handle insertions/deletions robustly. It is a greedy clustering approach, not the full CD-HIT program.
