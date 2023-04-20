def split_fasta_by_N(path_to_fasta_file):
    header = None
    with open(path_to_fasta_file) as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if line.startswith(">"):
                index = 0   
                if header:
                    # Split the sequence by N's
                    
                    seq_splits = filter(None, "".join(seq).split('N'))
                    # Yield the split sequences with new headers
                    for j, seq_split in enumerate(seq_splits):
                        seq_header = f"{header}_{index}"
                        yield seq_header, seq_split
                        index += 1
                header = line[1:]
                seq = []
            else:
                seq.append(line)
        if header:
            # Split the sequence by N's
            seq_splits = filter(None, "".join(seq).split('N'))
            # Yield the split sequences with new headers
            for j, seq_split in enumerate(seq_splits):
                seq_header = f"{header}_{index}"
                yield seq_header, seq_split
                index += 1