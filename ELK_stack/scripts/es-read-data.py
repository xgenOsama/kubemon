from elasticsearch7 import Elasticsearch
es = Elasticsearch("http://localhost:9200")

query = {
"bool": {
    "must": {
    "match": {      
        "status_code": "200"
    }
    }
}
}

resp = es.search(index="python-nginx-index", query=query)
print(resp['hits']['hits'][0]['_source'])