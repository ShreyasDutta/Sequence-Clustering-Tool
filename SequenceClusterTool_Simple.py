
def read_fasta(filename):
    sequences = {}
    current_name = ""
    current_seq = []

    with open(filename, "r") as file:
        for line in file:
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
def parse_fasta_text(text):
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
def calculate_gc(seq):
    if len(seq) == 0:
        return 0.0
    g_count = seq.count("G")
    c_count = seq.count("C")
    gc_percent = ((g_count + c_count) / len(seq)) * 100
    return round(gc_percent, 2)

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


def cluster_sequences(sequences, threshold=80.0):
    clusters = []

    for name in sequences:
        placed = False
        seq = sequences[name]

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

    return clusters

if __name__ == "__main__":
    print("==================================================")
    print("        SEQUENCE CLUSTERING TOOL")
    print("==================================================")

    filename = input("\nEnter the FASTA file path: ")
    test_sequences = read_fasta(filename)

    threshold = float(input("Enter similarity threshold (0-100): "))

    print(f"\nTotal Sequences: {len(test_sequences)}")
    print(f"Similarity Threshold: {threshold}%\n")

    print("Sequences Loaded:")
    for name, seq in test_sequences.items():
        gc = calculate_gc(seq)
        print(f"  {name}: {seq} (Length: {len(seq)}, GC: {gc}%)")

    clusters = cluster_sequences(test_sequences, threshold=threshold)

    print("\n--------------------------------------------------")
    print(f"CLUSTERING RESULTS: Found {len(clusters)} Clusters")
    print("--------------------------------------------------")

    for i, cluster in enumerate(clusters, start=1):
        print(f"\nCluster {i} (Members: {len(cluster)}):")

        for member_name in cluster:
            print(f"   -> {member_name} ({test_sequences[member_name]})")

    print("\n==================================================")
    print("Done!")
