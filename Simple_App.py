"""
====================================================================
PROJECT: Sequence Clustering Tool (Simple Desktop App)
STUDENT: Shreyas Dutta | ROLL NO: Se25ucab011
====================================================================
A simple graphical desktop interface (GUI) using Python's built-in tkinter.
No complex libraries needed!
====================================================================
"""

import tkinter as tk
from tkinter import messagebox


def calculate_gc(seq):
    if len(seq) == 0:
        return 0.0
    g = seq.count("G")
    c = seq.count("C")
    return round(((g + c) / len(seq)) * 100, 2)


def calculate_similarity(seq1, seq2):
    matches = 0
    min_len = min(len(seq1), len(seq2))
    for i in range(min_len):
        if seq1[i] == seq2[i]:
            matches += 1
    max_len = max(len(seq1), len(seq2))
    if max_len == 0:
        return 100.0
    return (matches / max_len) * 100


def parse_fasta_text(text):
    """Parses text containing >Header and sequence lines into a dictionary."""
    sequences = {}
    current_name = ""
    current_seq = []

    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if current_name:
                sequences[current_name] = "".join(current_seq)
            current_name = line[1:].strip()
            current_seq = []
        else:
            current_seq.append(line.upper())

    if current_name:
        sequences[current_name] = "".join(current_seq)

    return sequences


def run_clustering():
    raw_text = input_box.get("1.0", tk.END).strip()
    if not raw_text:
        messagebox.showwarning("Warning", "Please enter some sequences in FASTA format!")
        return

    try:
        threshold = float(thresh_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Similarity threshold must be a number (e.g., 80)!")
        return

    # 1. Parse sequences
    sequences = parse_fasta_text(raw_text)
    if not sequences:
        messagebox.showerror("Error", "No valid FASTA sequences found. Headers must start with '>'")
        return

    # 2. Perform simple clustering
    clusters = []
    for name in sequences:
        seq = sequences[name]
        placed = False

        for cluster in clusters:
            rep_name = cluster[0]
            rep_seq = sequences[rep_name]
            score = calculate_similarity(seq, rep_seq)
            if score >= threshold:
                cluster.append(name)
                placed = True
                break

        if not placed:
            clusters.append([name])

    # 3. Display output
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Found {len(clusters)} Cluster(s) at {threshold}% similarity threshold:\n\n")

    for i, cluster in enumerate(clusters, start=1):
        output_box.insert(tk.END, f"================ CLUSTER {i} ================\n")
        output_box.insert(tk.END, f"Representative: {cluster[0]}\n")
        output_box.insert(tk.END, f"Number of Members: {len(cluster)}\n")
        output_box.insert(tk.END, "Sequences:\n")
        for member in cluster:
            seq = sequences[member]
            gc = calculate_gc(seq)
            output_box.insert(tk.END, f"  • {member} (Len: {len(seq)}, GC: {gc}%)\n     {seq}\n")
        output_box.insert(tk.END, "\n")


def load_sample_data():
    sample = (
        ">Sequence_1\nATGCGTACGTAG\n"
        ">Sequence_2\nATGCGTACGTAA\n"
        ">Sequence_3\nATGCGTACGTAC\n"
        ">Sequence_4\nGGCTAACCGGTT\n"
        ">Sequence_5\nGGCTAACCGGTA\n"
    )
    input_box.delete("1.0", tk.END)
    input_box.insert(tk.END, sample)


# ====================================================================
# TKINTER WINDOW SETUP
# ====================================================================
root = tk.Tk()
root.title("Sequence Clustering Tool - Shreyas Dutta (Se25ucab011)")
root.geometry("700x650")

# Title Header
header = tk.Label(root, text="DNA Sequence Clustering Tool", font=("Arial", 16, "bold"), fg="#1e3a8a")
header.pack(pady=8)
sub_header = tk.Label(root, text="Student: Shreyas Dutta | Roll No: Se25ucab011", font=("Arial", 10, "italic"))
sub_header.pack()

# Input Label & Buttons
frame_top = tk.Frame(root)
frame_top.pack(fill=tk.X, padx=15, pady=5)
lbl_input = tk.Label(frame_top, text="Input Sequences (FASTA format):", font=("Arial", 10, "bold"))
lbl_input.pack(side=tk.LEFT)
btn_sample = tk.Button(frame_top, text="Load Sample Data", command=load_sample_data, bg="#e2e8f0")
btn_sample.pack(side=tk.RIGHT)

# Text Box for Sequences
input_box = tk.Text(root, height=8, font=("Courier", 10))
input_box.pack(fill=tk.X, padx=15, pady=2)

# Controls (Threshold & Run Button)
frame_ctrl = tk.Frame(root)
frame_ctrl.pack(fill=tk.X, padx=15, pady=10)

lbl_thresh = tk.Label(frame_ctrl, text="Similarity Threshold (%):", font=("Arial", 10))
lbl_thresh.pack(side=tk.LEFT)

thresh_entry = tk.Entry(frame_ctrl, width=6, font=("Arial", 10))
thresh_entry.insert(0, "80")
thresh_entry.pack(side=tk.LEFT, padx=8)

btn_run = tk.Button(frame_ctrl, text="▶ Cluster Sequences", font=("Arial", 11, "bold"), bg="#2563eb", fg="white", padx=12, command=run_clustering)
btn_run.pack(side=tk.RIGHT)

# Output Results Box
lbl_output = tk.Label(root, text="Clustering Results:", font=("Arial", 10, "bold"))
lbl_output.pack(anchor=tk.W, padx=15, pady=(5, 0))

output_box = tk.Text(root, height=14, font=("Courier", 10), bg="#f8fafc")
output_box.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

# Load sample data automatically on open
load_sample_data()

if __name__ == "__main__":
    root.mainloop()
