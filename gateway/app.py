import json
import logging
import re

from flask import Flask
from Levenshtein import distance

app = Flask(__name__)

logging.basicConfig(filename='record.log', level=logging.DEBUG)

@app.route('/')
def hello():

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
            # data.append(f.read())
            data[file] = f.read().splitlines()
            del data[file][0::2]
            del data[file][1::2]
            data['refGen'] = REFERENCE_GENOME
            # data[file+'count'] = len(data[file])
        # f = open("demofile.txt", "r")
        #     print(f.read())
    
    # app.logger.info('test', 'teseting')
            
    r2_reads = [file for file in files if re.search("_R2_", file)]

    # for file

    for reads in r2_reads:
        print(reads)
        # print(data[reads])
        for read in data[reads]:
            geneMatch = {
                'gene': {},
                'variant': {},
                'levenshtein_distance': 9999999
            }
            for gene in REFERENCE_GENOME:
                print(gene)
                for variant in gene['data']['variants']:
                    print('var', variant['sequence'])
                    print('read', read)
                    print('ld', distance(variant['sequence'], read))
                    # print('var', variant.sequence)
                    if distance(variant['sequence'], read) < geneMatch['levenshtein_distance']:
                        geneMatch['gene'] = gene['gene']
                        geneMatch['variant'] = variant
                        geneMatch['levenshtein_distance'] = distance(variant['sequence'], read)
            print('match', geneMatch)
        data[reads] = geneMatch
    
    print(r2_reads)

    # print(distance('ATGGCCACTGTTCGAGCTCTTTTGCCAAATCTTTCATTTTAGTCACTTTGTGCATCAAGGTTCGAGAGAGGGACAGGGCGATGAAAACCGGTCGGATATATGACGCTGATGCAGCAACTTAACCGTTACCAAACCCCGTAGCGGATCGCATGATCTCTTGAACCGTGAGTGAAGTGTCGCCTGGACCCTTGGCGTGGCAA', 'ATGGCCACTGTTCGAGCTCTTTTGCCAAATCTTTCATTTTAGTCACTTTGTGCATCAAGGTTCGAGAGAGGGACAGGGCGATGAAAACCGGTCGGATATATGAC'))    

    return data

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8000)