from elasticsearch import Elasticsearch
import configparser
import json

def query(q, disp_mode):
    es = Elasticsearch()

    index_name = 'ptt_search_latest'
    type_ = 'test_type'

    q = '('+q+')'

    if '&' in q:
        q = q.replace('&', ') AND (')
    elif '|' in q:
        q = q.replace('&', ') OR (')

    search_params = {
        'query':{
            'query_string':{
                'query': q,
                'default_field': 'artical'
            }
        }
    }
    result = es.search(index=index_name, doc_type=type_, body=search_params)
    if len(result['hits']['hits']) > 10:
        result = result['hits']['hits'][0:10]
    else:
        result = result['hits']['hits'][0:-1]
        
    

    for i in range(len(result)):
        # _score
        print('Score: ' + str(result[i]['_score']))
        print('看版: ' + str(result[i]['_source']['board']))
        print('標題: ' + str(result[i]['_source']['title']))
        print('作者: ' + str(result[i]['_source']['author']))
        if disp_mode == 'complete':
            print('內文: ' + str(result[i]['_source']['artical']))
        print('***************************************************')

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    disp = config['setting']['display_mode']
    
    while True:
        q = input('Please enter the search query...\n')
        if q == 'exit':
            break
        query(q, disp)
