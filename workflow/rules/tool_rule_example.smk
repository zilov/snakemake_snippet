rule get_coverage_hifi:
    input:
        hifi = HIFI, # you could use global variables in rules
        assembly_splitted_by_n = rules.script_rule.output.splitted_assembly, ## connect rules outputs to build pipeline 
    threads: workflow.cores ## workflow cores are set in wrapper.py script
    conda: envs.align ## path to env file is in Snakefile
    output:
        alignment_bam = f"{OUTDIR}/alignment/{PREFIX}_sorted.bam",  # you could use f strings in rules
        alignment_stats = f"{OUTDIR}/alignment/{PREFIX}_sorted.stats", # it could be several output files
        coverage_bed = f"{OUTDIR}/alignment/{PREFIX}_coverage.bed",
    params: ## in params you could set run parameters 
        prefix = PREFIX, 
        outdir = directory(f"{OUTDIR}/alignment") # directory() creates folder before run
    shell: """
    minimap2 -ax map-hifi {input.assembly_splitted_by_n} {input.hifi} -t {threads} \
    | samtools view -b -u - \
    | samtools sort -@ {threads} -T tmp > {output.alignment_bam} \
    && samtools flagstat {output.alignment_bam} > {output.alignment_stats} \
    && bedtools genomecov -bga -split -ibam {output.alignment_bam} > {output.coverage_bed}
    """