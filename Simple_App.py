
import tkinter as tk
from tkinter import messagebox, filedialog

from SequenceClusterTool_Simple import (
    parse_fasta_text,
    calculate_gc,
    cluster_sequences
)


def browse_fasta_file():
    filename = filedialog.askopenfilename(
        title="Select FASTA File",
        filetypes=[
            ("FASTA Files", "*.fasta *.fa *.fna *.fas"),
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if filename:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                fasta_text = file.read()

            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, fasta_text)

            file_label.config(text=filename.split("/")[-1])

        except (OSError, UnicodeError) as e:
            messagebox.showerror("File Error", str(e))


def run_clustering():
    raw_text = input_box.get("1.0", tk.END).strip()

    if not raw_text:
        messagebox.showwarning("Warning", "Please upload or enter FASTA sequences!")
        return

    try:
        threshold = float(thresh_entry.get())

        if threshold < 0 or threshold > 100:
            raise ValueError

    except ValueError:
        messagebox.showerror("Error", "Enter a threshold between 0 and 100!")
        return

    sequences = parse_fasta_text(raw_text)

    if not sequences:
        messagebox.showerror("Error", "No valid FASTA sequences found!")
        return

    clusters = cluster_sequences(sequences, threshold)

    output_box.delete("1.0", tk.END)

    output_box.insert(
        tk.END,
        f"Found {len(clusters)} Cluster(s) at {threshold}% similarity threshold:\n\n"
    )

    for i, cluster in enumerate(clusters, start=1):
        output_box.insert(tk.END, f"================ CLUSTER {i} ================\n")
        output_box.insert(tk.END, f"Representative: {cluster[0]}\n")
        output_box.insert(tk.END, f"Number of Members: {len(cluster)}\n")
        output_box.insert(tk.END, "Sequences:\n")

        for member in cluster:
            seq = sequences[member]
            gc = calculate_gc(seq)

            output_box.insert(
                tk.END,
                f"  {member} (Len: {len(seq)}, GC: {gc}%)\n     {seq}\n"
            )

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
    file_label.config(text="Sample data loaded")


root = tk.Tk()
root.title("Sequence Clustering Tool")
root.geometry("750x680")

header = tk.Label(
    root,
    text="DNA Sequence Clustering Tool",
    font=("Arial", 16, "bold"),
    fg="#1e3a8a"
)
header.pack(pady=8)

sub_header = tk.Label(
    root,
    text="Sequence Clustering Project",
    font=("Arial", 10, "italic")
)
sub_header.pack()


frame_top = tk.Frame(root)
frame_top.pack(fill=tk.X, padx=15, pady=8)

lbl_input = tk.Label(
    frame_top,
    text="Input Sequences (FASTA format):",
    font=("Arial", 10, "bold")
)
lbl_input.pack(side=tk.LEFT)

btn_browse = tk.Button(
    frame_top,
    text="Browse FASTA File",
    command=browse_fasta_file,
    bg="#dbeafe"
)
btn_browse.pack(side=tk.RIGHT, padx=5)

btn_sample = tk.Button(
    frame_top,
    text="Load Sample Data",
    command=load_sample_data,
    bg="#e2e8f0"
)
btn_sample.pack(side=tk.RIGHT, padx=5)


file_label = tk.Label(
    root,
    text="No file selected",
    font=("Arial", 9, "italic"),
    fg="gray"
)
file_label.pack(anchor=tk.W, padx=15)


input_box = tk.Text(root, height=9, font=("Courier", 10))
input_box.pack(fill=tk.X, padx=15, pady=5)


frame_ctrl = tk.Frame(root)
frame_ctrl.pack(fill=tk.X, padx=15, pady=10)

lbl_thresh = tk.Label(
    frame_ctrl,
    text="Similarity Threshold (%):",
    font=("Arial", 10)
)
lbl_thresh.pack(side=tk.LEFT)

thresh_entry = tk.Entry(frame_ctrl, width=6, font=("Arial", 10))
thresh_entry.insert(0, "80")
thresh_entry.pack(side=tk.LEFT, padx=8)

btn_run = tk.Button(
    frame_ctrl,
    text="Cluster Sequences",
    font=("Arial", 11, "bold"),
    bg="#2563eb",
    fg="white",
    padx=12,
    command=run_clustering
)
btn_run.pack(side=tk.RIGHT)


lbl_output = tk.Label(
    root,
    text="Clustering Results:",
    font=("Arial", 10, "bold")
)
lbl_output.pack(anchor=tk.W, padx=15, pady=(5, 0))

output_box = tk.Text(
    root,
    height=16,
    font=("Courier", 10),
    bg="#f8fafc"
)
output_box.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)


load_sample_data()

if __name__ == "__main__":
    root.mainloop()
