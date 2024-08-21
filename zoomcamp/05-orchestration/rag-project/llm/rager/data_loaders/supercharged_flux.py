from typing import Dict, List, Union

import numpy as np
from elasticsearch import Elasticsearch, exceptions


@data_loader
def search(*args, **kwargs) -> List[Dict]:
    """
    query_embedding: Union[List[int], np.ndarray]
    """
    
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name = kwargs.get('index_name', 'documents')
    source = kwargs.get('source', "cosineSimilarity(params.query_vector, 'question') + 1.0")
    top_k = kwargs.get('top_k', 5)
    chunk_column = kwargs.get('chunk_column', 'content')


    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": source,
                "params": {"query_vector": "When is the next cohort?"},
            }
        }
    }

    print("Sending script query:", script_query)

    es_client = Elasticsearch(connection_string)
    
    try:
        response = es_client.search(
            index=index_name,
            body={
                "size": top_k,
                "query": script_query,
                "_source": [chunk_column],
            },
        )

        print("Raw response from Elasticsearch:", response)

        return [hit['_source'][chunk_column] for hit in response['hits']['hits']]
    
    except exceptions.BadRequestError as e:
        print(f"BadRequestError: {e.info}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []