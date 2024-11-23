import json
import logging
import re
import time

from flask import Flask
from Levenshtein import distance

app = Flask(__name__)

logging.basicConfig(filename='logs.log', level=logging.INFO)

@app.route('/')
def hello():
    tic = time.perf_counter_ns()
    REFERENCE_GENOME = []
    with open("./reference_genome.json", "r") as f:
        REFERENCE_GENOME = json.load(f)

    files = (
        'tinygex_S1_L001_R1_001.fastq',
        'tinygex_S1_L001_R2_001.fastq',
        'tinygex_S1_L002_R1_001.fastq',
        'tinygex_S1_L002_R2_001.fastq',
    )

    data = {}
	
    for file in files:
        with open('./data/' + file, 'r') as f:
            data[file] = f.read().splitlines()
            del data[file][0::2]
            del data[file][1::2]
            data['refGen'] = REFERENCE_GENOME

    r1_reads = [file for file in files if re.search("_R1_", file)]        
    r2_reads = [file for file in files if re.search("_R2_", file)]

    data['count_matrix'] = {
        'cells': [],
        'umis': [],
        'data': {}
    }  

    for reads in r2_reads:
        for index, read in enumerate(data[reads]):
            gene_match = {
                'gene': {},
                'variant': {},
                'levenshtein_distance': 9999999
            }
            for gene in REFERENCE_GENOME:
                for variant in gene['data']['variants']:
                    if distance(variant['sequence'], read) < gene_match['levenshtein_distance']:
                        gene_match['gene'] = gene['gene']
                        gene_match['variant'] = variant
                        gene_match['levenshtein_distance'] = distance(variant['sequence'], read)
            data['count_matrix']['data']
            data[reads][index] = gene_match


    for reads_index, reads in enumerate(r1_reads):
        for read_index, read in enumerate(data[reads]):
            bc = read[0:18]
            umi = read[18:]
            if bc not in data['count_matrix']['cells']:
                data['count_matrix']['cells'].append(bc)
                genes = {}
                for gene in REFERENCE_GENOME:
                    genes[gene['gene']] = 0
                data['count_matrix']['data'][bc] = {
                    'genes': genes
                }
            if umi not in data['count_matrix']['umis']:
                data['count_matrix']['umis'].append(umi)
                data['count_matrix']['data'][bc]['genes'][data[r2_reads[reads_index]][read_index]['gene']] = data['count_matrix']['data'][bc]['genes'][data[r2_reads[reads_index]][read_index]['gene']] + 1
            else:
                app.logger.info('Removing duplicate UMI' + umi)  

    app.logger.info('Elapsed: ' + str((time.perf_counter_ns() - tic) / 1000000) + 'ns')

    # Also printing in case of logging config doesn't work out of the box
    print('Elapsed: ' + str((time.perf_counter_ns() - tic) / 1000000) + 'ns')

    return data

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8000)