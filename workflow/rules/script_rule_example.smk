from scripts.script import split_fasta_by_N

rule script_rule:
    input:
        assembly = ASSEMBLY
    output:
        splitted_assembly = f"{OUTDIR}/splitted_assmbly.fasta"
    run:
        with open(output.splitted_assembly, 'w') as fw:
            for header, seq in split_fasta_by_N(input.assembly):
                fw.write(f">{header}\n{seq}\n")