from elasticsearch7 import Elasticsearch
es = Elasticsearch("http://localhost:9200", http_auth=('company1', 'password'))

query = {
"bool": {
    "must": {
    "match": {      
        "host.name": "docker-desktop"
    }
    }
}
}

resp = es.search(index="nginx-logs-*", query=query)

# iterate the nested dictionaries inside the ["hits"]["hits"] list
for num, doc in enumerate(resp['hits']['hits']):
    print ("DOC ID:", doc["_id"], "--->", doc, type(doc), "\n")

    # Use 'iteritems()` instead of 'items()' if using Python 2
    for key, value in doc.items():
        print (key, "-->", value)

    # print a few spaces between each doc for readability
    print ("\n\n")