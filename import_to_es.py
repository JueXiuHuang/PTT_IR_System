from elasticsearch import Elasticsearch, helpers
import json

ptt_mapping = {
    'properties':{
        'board':{
            'type':'keyword'
        },
        'title':{
            'type':'text'
        },
        'author':{
            'type':'keyword'
        },
        'artical':{
            'type':'text'
        }
    }
}

renames_key = {
    'board': 'board',
    'title': 'title',
    'author': 'author',
    'artical': 'artical',
}

def read_data():
    with open('crawled_data_latest.json', 'r', encoding='utf-8') as f:
        for row in f:
            d = eval(row.strip())
            d = json.dumps(d, ensure_ascii=False)
            row = json.loads(d)

            for k, v in renames_key.items():
                for old_name in row:
                    if k == old_name:
                        row[v] = row.pop(old_name)
            yield row

def load_to_es():
    
    index_name = 'ptt_search_latest'
    type_ = 'test_type'
    es = Elasticsearch()

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
    print('Index created!')

    if not es.indices.exists_type(index=index_name, doc_type=type_):
        es.indices.put_mapping(
            index=index_name, doc_type=type_, body=ptt_mapping, include_type_name=True)
    print('Mappings created!')

    success, _ = helpers.bulk(
        client=es, actions=read_data(), index=index_name, doc_type=type_, ignore=400)
    print('success: ', success)

if __name__ == '__main__':
    load_to_es()