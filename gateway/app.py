import datetime
import json
import logging
import re
import requests
import time

import db

from flask import Flask, request
from flask_cors import CORS
from Levenshtein import distance
import numpy as np
from playhouse.shortcuts import model_to_dict
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

app = Flask(__name__)

CORS(app, origins=['http://localhost:5173'])

logging.basicConfig(filename=f'./logs/{str(datetime.date.today()).replace("-", "_")}.log', level=logging.INFO)

routes = {
    '/': {
        'public': True
    },
    '/data/<int:sample_id>': {
        'public': True
    }
}

hosts_whitelist = {
    None: True,
    'localhost': True
}

@app.before_request
def authorization_placeholder():
    if request.routing_exception:
        app.logger.info('Routing exception: ' + str(request.routing_exception))
        return {
            'error': str(request.routing_exception)
        }
    if routes[str(request.url_rule)]['public'] == False:
        app.logger.info('Unauthorized request: ' + str(request.url_rule))
        return {
            "error": "Not authorized"
        }

@app.route('/data/<int:sample_id>', methods=['GET'])
def sample_data(sample_id):
    tic = time.perf_counter_ns()

    stored_run_data = {}
    try:
        stored_run_data = db.Run.get(id=(sample_id))
        app.logger.info('Elapsed: ' + str((time.perf_counter_ns() - tic) / 1000000) + 'ns')

        # Also printing in case of logging config doesn't work out of the box
        print('Elapsed: ' + str((time.perf_counter_ns() - tic) / 1000000) + 'ns')
        return json.loads(stored_run_data.data)
    except db.DoesNotExist:
        app.logger.info('Run data not found, analyzing for storage: ' + str(sample_id))

    REFERENCE_GENOME = []
    with open("./reference_genome.json", "r") as f:
        REFERENCE_GENOME = json.load(f)

    files = (
        f'tinygex_S{sample_id}_L001_R1_001.fastq',
        f'tinygex_S{sample_id}_L001_R2_001.fastq',
        f'tinygex_S{sample_id}_L002_R1_001.fastq',
        f'tinygex_S{sample_id}_L002_R2_001.fastq',
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
                        # This will work, it's just slow and needs to be reduced to a single http call
                        # r = requests.post('http://localhost:8443/levenshtein', json={
                        #     'target_sequence': variant['sequence'],
                        #     'read_sequence': read
                        # })
                        # print(r, distance(variant['sequence'], read))
                        gene_match['levenshtein_distance'] = distance(variant['sequence'], read)
            data['count_matrix']['data']
            data[reads][index] = gene_match

    # r = requests.post('http://localhost:8443/levenshtein', json={
    #     'target_sequence': variant['sequence'],
    #     'read_sequence': read
    # })

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

    clustering_array = []

    for cell in data['count_matrix']['data']:
        genes = list(data['count_matrix']['data'][cell]["genes"].keys())
        genes.sort()
        print(genes)
        count = []
        for gene in genes:
            print(data['count_matrix']['data'][cell]["genes"][gene])
            count.append(data['count_matrix']['data'][cell]["genes"][gene])
        print(count)
        clustering_array.append(count)

    clustering_array = np.array(clustering_array)
    print('cu', clustering_array)
    
    sil_score_max = -1 #this is the minimum possible score

    best_n_clusters = 0
    for n_clusters in range(2,len(data['count_matrix']['data'])):
        model = KMeans(n_clusters = n_clusters, init='k-means++', max_iter=100, n_init=1)
        labels = model.fit_predict(clustering_array)
        sil_score = silhouette_score(clustering_array, labels)
        print("The average silhouette score for %i clusters is %0.2f" %(n_clusters,sil_score))
        if sil_score > sil_score_max:
            sil_score_max = sil_score
            best_n_clusters = n_clusters
    data['clusters'] = {}
    data['clusters']['clusters'] = best_n_clusters
    data['clusters']['clustering_array'] = clustering_array.tolist()
    db.Run.create(id=sample_id, data=json.dumps(data))

    return data

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8000)