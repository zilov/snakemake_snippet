# snakemake_snippet
Snippet for snakemake pipelines. Use it to create your pipelines, just change files.

Command files commented in key points. Snippet has example of rules with python code and tools installed automaticly with `conda`. This snippet is runnable, it needs only `snakemake` available in you environment.

# Structure
* `argparse_wrapper.py` - scripts ahat parses arguments, creates config files and runs snakemake
* `workflow/Snakefile` - main pipeline file, collects rules needed for run and structure of the pipeline
* `workflow/rules` - folder with rules to run
* `workflow/envs` - folder with conda env settings for rules 
* `workflow/scripts` - example of script used in one rule
* `test` - folder with files needed to test snippet

# Usage
Clone the repository and try to run snippet, for example:
 `./argparse_wrapper.py -a ./test/assembly_with_Ns.fasta -hifi ./test/hifi_reads.fastq -o ./test/test_output -d`
This command will dry run the script and list a steps to be done. Delete `-d` to run pipeline.