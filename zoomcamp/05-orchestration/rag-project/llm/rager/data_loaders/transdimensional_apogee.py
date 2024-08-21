from typing import Dict, List, Union

import numpy as np
from elasticsearch import Elasticsearch, exceptions


@data_loader
def search(*args, **kwargs) -> List[Dict]:
    """
    query_embedding: Union[List[int], np.ndarray]
    """
    
    connection_string = kwargs.get('connection_string', 'http://host.docker.internal:9200')
    
    index_name = kwargs['index_name']
    
    top_k = kwargs.get('top_k', 5)

    query = {
    "query": {
        "match": {
            "question": "When is the next cohort?"
            }
        }
    }

    es_client = Elasticsearch(connection_string)
    
    try:
        response = es_client.search(
            index=index_name,
            body=query
        )

        return response['hits']['hits'][0]['_id']
    
    except exceptions.BadRequestError as e:
        print(f"BadRequestError: {e.info}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []