import os
from redun import task, File, cond

SAMTOOLS = 'tools/samtools-1.16.1/samtools'
BWA = 'tools/bwa/bwa'
CHECKER_SCRIPT = 'result_checker.py'
FASTQC = 'tools/FastQC/fastqc'
FREEBAYES = 'freebayes'

OUTPUT_DIR = 'output'
LOG_DIR = 'logs'

redun_namespace = "bioinformatics.genoms"

ref_genome = 'ref_genome/GCF_000005845.2_ASM584v2_genomic.fna'
target_genome = 'SRR20043616.fastq'
bam_file = f'{OUTPUT_DIR}/result.bam'
bam_sorted_file = f'{OUTPUT_DIR}/result.sorted.bam'
aligned_gz = f'{OUTPUT_DIR}/aligned.gz'
txt_file = f'{OUTPUT_DIR}/flagstat.txt'
сheck_res = f'{OUTPUT_DIR}/results.txt'
vcf_res = f'{OUTPUT_DIR}/results.vcf'

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

@task
def generate_fasqc_report(target_genome):
    os.system(f'{FASTQC} -o {OUTPUT_DIR} {target_genome} &> {LOG_DIR}/fastqc.log')
    return File(f'{OUTPUT_DIR}/{target_genome.split(".")[0]}_fastqc.html')

@task
def align(ref_genome: str, target_genome: str) -> File:
    os.system(f'{BWA} index {ref_genome} &> {LOG_DIR}/index.log && {BWA} mem {ref_genome} {target_genome} 2> {LOG_DIR}/align.log | gzip -3 > {aligned_gz}')
    return File(aligned_gz)

@task
def sam2bam(aligned_gz: File, bam_file: str) -> File:
    os.system(f'{SAMTOOLS} view -Sb -o {bam_file} {aligned_gz.path} &> {LOG_DIR}/sam2bam.log')
    return File(bam_file)

@task
def flagstat(bam_file_processed: File, txt_file: str) -> File:
    os.system(f'{SAMTOOLS} flagstat {bam_file_processed.path} > {txt_file}')
    return File(txt_file)

@task
def check_results(txt_file_processed: File, сheck_res: str) -> File:
    os.system(f'python {CHECKER_SCRIPT} {txt_file_processed.path} > {сheck_res}')
    with open(сheck_res) as res:
        return 'OK' in res.read()

@task
def samtools_sort(bam_file_processed: File, bam_sorted_file: str) -> File:
    os.system(f'{SAMTOOLS} sort {bam_file_processed.path} > {bam_sorted_file} 2> {LOG_DIR}/sort.log')
    return File(bam_sorted_file)

@task
def generate_vcf(ref_genome: str, bam_sorted_file: File, vcf_res: str) -> File:
    os.system(f'{FREEBAYES} -f {ref_genome} {bam_sorted_file.path} > {vcf_res} 2> {LOG_DIR}/freebayes.log')
    return File(vcf_res)

@task()
def main(ref_genome=ref_genome, target_genome=target_genome) -> File:
    fast_qc_report = generate_fasqc_report(target_genome)

    aligned_gz_processed = align(ref_genome, target_genome)
    bam_file_processed = sam2bam(aligned_gz_processed, bam_file)
    txt_file_processed = flagstat(bam_file_processed, txt_file)

    is_ok = check_results(txt_file_processed, сheck_res)
    bam_sorted_file_processed = samtools_sort(bam_file_processed, bam_sorted_file)
    vcf_res_processed = generate_vcf(ref_genome, bam_sorted_file_processed, vcf_res)

    return fast_qc_report, cond(is_ok, vcf_res_processed, 'Less then 90%, stopping')


@task
def generate_pipeline_visualisation() -> bool:
    logs = os.popen('redun log | grep "main.py main"').read()
    for log_line in logs.split('\n'):
        if 'DONE' in log_line:
            latest_log = logs.split('\n')[0]
            run_id = latest_log.split(' ')[1]
            os.system(f'redun viz --output {OUTPUT_DIR}/viz {run_id}')
            return True
    return False