#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#@created: 16.02.2023
#@author: Danil Zilov
#@contact: zilov.d@gmail.com

import argparse
import os
import os.path
from inspect import getsourcefile
from datetime import datetime
import yaml
import sys

## generates config file which is used by Snakemake
def config_maker(settings, config_file):
    if not os.path.exists(os.path.dirname(config_file)):
        os.mkdir(os.path.dirname(config_file))
    with open(config_file, "w") as f:
        yaml.dump(settings, f)
        print(f"CONFIG IS CREATED! {config_file}")
        

def check_input(path_to_file):
    if not os.path.isfile(path_to_file) or os.path.getsize(path_to_file) == 0:
        raise ValueError(f"The file '{path_to_file}' does not exist or empty. Check arguemnts list!")
    return os.path.abspath(path_to_file)

def main(settings):        
    if settings["debug"]:
        snake_debug = "-n"
    else:
        snake_debug = ""

    #Snakemake
    command = f"""
    snakemake --snakefile {settings["execution_folder"]}/workflow/Snakefile \
              --configfile {settings["config_file"]} \
              --cores {settings["threads"]} \
              --use-conda {snake_debug}"""
    print(command)
    os.system(command)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process assembly fasta and coverage bed files.')
    parser.add_argument("-m", "--mode", help="mode to use", 
                        choices=["hifi", "paired_reads", "nanopore", "pacbio", "coverage"], default="hifi")
    parser.add_argument('-a', '--assembly', type=str, help='Path to the assembly fasta file.', required=True)
    parser.add_argument("-hifi", type=str, help='Path to the hifi reads fastq file.', default="")
    parser.add_argument('-t','--threads', type=int, help='number of threads [default == 8]', default = 8)
    parser.add_argument('-p', '--prefix', help="output files prefix (assembly file prefix by default)", default='')
    parser.add_argument('-o', '--output_folder', type=str, default="./asShredder", help='Path to the output folder.')
    parser.add_argument('-d','--debug', help='debug mode', action='store_true') ## run in debug mode to check if everything is ok
        
    args = parser.parse_args()
    
    ## parse args
    mode = args.mode
    assembly = check_input(args.assembly)
    hifi = check_input(args.hifi)
    output_folder = os.path.abspath(args.output_folder)
    debug = args.debug
    threads = args.threads
    prefix = os.path.splitext(os.path.basename(assembly))[0] if not args.prefix else args.prefix
    
    ## run settings
    execution_folder = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))
    execution_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    config_file = os.path.join(execution_folder, f"config/config_{execution_time}.yaml")
    run_folder = os.getcwd()
    command = " ".join(sys.argv)
    
    ## change to execution folder to not regenerate snakemake env files
    os.chdir(execution_folder)
            
    # set settings to create config and run tool
    settings = {
        "command" : command,
        "run_folder": run_folder,
        "mode" : mode,
        "assembly": assembly,
        "hifi": hifi,
        "outdir" : output_folder,
        "execution_folder" : execution_folder,
        "prefix" : prefix,
        "debug": debug,
        "config_file" : config_file,
        "threads" : threads
    }
    
    config_maker(settings, config_file)
    main(settings)