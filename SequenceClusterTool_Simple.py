"""
====================================================================
PROJECT: Sequence Clustering Tool (Simple & Clean Version)
STUDENT: Shreyas Dutta | ROLL NO: Se25ucab011
====================================================================
This program:
1. Reads DNA sequences from a FASTA file or text.
2. Calculates GC content for each sequence.
3. Compares sequences to calculate percentage similarity.
4. Groups similar sequences into real Clusters based on a threshold (e.g., 80%).
====================================================================
"""

def read_fasta(filename):
    """
    Reads a FASTA file and returns a dictionary: {sequence_name: sequence_dna}
    """
    sequences = {}
    current_name = ""
    current_seq = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                # Save previous sequence if it exists
                if current_name:
                    sequences[current_name] = "".join(current_seq)
                current_name = line[1:].strip()  # Remove '>'
                current_seq = []
            else:
                current_seq.append(line.upper())

        # Save the last sequence in the file
        if current_name:
            sequences[current_name] = "".join(current_seq)

    return sequences


def calculate_gc(seq):
    """
    Calculates GC percentage: (G + C) / length * 100
    """
    if len(seq) == 0:
        return 0.0
    g_count = seq.count("G")
    c_count = seq.count("C")
    gc_percent = ((g_count + c_count) / len(seq)) * 100
    return round(gc_percent, 2)


def calculate_similarity(seq1, seq2):
    """
    Compares two sequences character by character.
    Returns percentage of matching characters.
    """
    matches = 0
    min_len = min(len(seq1), len(seq2))

    for i in range(min_len):
        if seq1[i] == seq2[i]:
            matches += 1

    max_len = max(len(seq1), len(seq2))
    if max_len == 0:
        return 100.0

    return (matches / max_len) * 100


def cluster_sequences(sequences, threshold=80.0):
    """
    Groups sequences into clusters based on similarity threshold.
    
    Logic:
    - Take each sequence one by one.
    - Check if it is similar (>= threshold) to the representative of an existing cluster.
    - If yes, add it to that cluster.
    - If no, create a brand new cluster with this sequence.
    """
    clusters = []  # List of clusters: each cluster is a list of sequence names

    for name in sequences:
        placed = False
        seq = sequences[name]

        for cluster in clusters:
            # Compare with the first sequence (representative) of this cluster
            rep_name = cluster[0]
            rep_seq = sequences[rep_name]

            score = calculate_similarity(seq, rep_seq)
            if score >= threshold:
                cluster.append(name)
                placed = True
                break

        # If it doesn't match any existing cluster, make a new cluster
        if not placed:
            clusters.append([name])

    return clusters


# ====================================================================
# MAIN PROGRAM (Test with sample sequences)
# ====================================================================
if __name__ == "__main__":
    # Sample dictionary (same as your original Update 2 project)
    test_sequences = {
        "Sequence 1": "ATGCGTACGTAG",
        "Sequence 2": "ATGCGTACGTAA",
        "Sequence 3": "ATGCGTACGTAC",
        "Sequence 4": "GGCTAACCGGTT",
        "Sequence 5": "GGCTAACCGGTA"
    }

    threshold = 80.0

    print("==================================================")
    print("        SEQUENCE CLUSTERING TOOL")
    print("      Student: Shreyas Dutta (Se25ucab011)")
    print("==================================================")
    print(f"\nTotal Sequences: {len(test_sequences)}")
    print(f"Similarity Threshold: {threshold}%\n")

    # 1. Print sequences with GC content
    print("Sequences Loaded:")
    for name, seq in test_sequences.items():
        gc = calculate_gc(seq)
        print(f"  {name}: {seq} (Length: {len(seq)}, GC: {gc}%)")

    # 2. Run Clustering
    clusters = cluster_sequences(test_sequences, threshold=threshold)

    # 3. Display Results
    print("\n--------------------------------------------------")
    print(f"CLUSTERING RESULTS: Found {len(clusters)} Clusters")
    print("--------------------------------------------------")
    for i, cluster in enumerate(clusters, start=1):
        print(f"\nCluster {i} (Members: {len(cluster)}):")
        for member_name in cluster:
            print(f"   -> {member_name} ({test_sequences[member_name]})")

    print("\n==================================================")
    print("Done!")
