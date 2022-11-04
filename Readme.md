# Bioinformatics - Task 4
### Building a pipeline for obtaining genetic variants

## Requirements
1. conda for managing python environments
2. graphviz:  
   `apt-get install graphviz graphviz-dev`  
   or  
   `brew install graphviz`
3. [FastQC](https://github.com/s-andrews/FastQC) 
4. [samtools](https://github.com/samtools/samtools) 
5. [bwa](https://github.com/lh3/bwa) 

Tools 3,4,5 must be installed in the project's `tools` folder

## Download genome files:
1. Download [reference genome](https://www.ncbi.nlm.nih.gov/assembly/GCF_000005845.2/) and put `.fna` file in `ref_genome` folder
2. Download [sequencing result](https://www.ncbi.nlm.nih.gov/sra/?term=SRR20043616) and put `.fastq` file in the project root filder

## Preparing python environment
```
conda create -n bio python=3.10 
conda install --channel conda-forge pygraphviz
pip install redun "redun[viz]"
```

## Run
### To run main pipeline:  

```
conda activate bio
redun run main.py main
```
Logs will be saved to `logs` and results to `output`

### To make pipeline vizualization:

```
redun run main.py generate_pipeline_visualisation
```
Pipeline visualization wiil be saved to `output`

## Results
The repository contains the results of pipeline processing of the genomes specified in the section **Download genome files**.
