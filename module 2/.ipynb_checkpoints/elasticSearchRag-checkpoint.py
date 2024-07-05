import os
import json
import wget
from elasticsearch import Elasticsearch, BadRequestError
from tqdm.auto import tqdm

class ElasticSearchRag():
    def get_document(self):
        """
        Retrieve FAQ documents and format them for RAG
        """

        if not os.path.isfile("documents.json"):
            wget.download("https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json")
        else:
            print("documents.json already exists.")
        json_file = "documents.json"
        
        with open(json_file, "rt") as f_in:
            docs_raw = json.load(f_in)
        documents = []

        for course_dict in docs_raw:
            for doc in course_dict['documents']:
                doc['course'] = course_dict['course']
                documents.append(doc)
        return documents

    # def create_esIndex(self, es_client):
    def create_esIndex(self):
        index_settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "section": {"type": "text"},
                    "question": {"type": "text"},
                    "course": {"type": "keyword"} 
                }
            }
        }

        index_name = "course-questions"
        es_client = Elasticsearch('http://localhost:9200') 

        try:
            es_client.indices.create(index=index_name, body=index_settings)
            for doc in tqdm(self.get_document()):
                es_client.index(index=index_name, document=doc)
            # return es_client
        except BadRequestError:
            print(f"Elastic search index \"{index_name}\" already exist.")
            # return es_client