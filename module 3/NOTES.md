## Module 3: Vector Search
All module 3 videos and notebook links can be found [here](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/03-vector-search). All module 3 notebooks are executed in existing conda environment ```llm-zoomcamp-env``` with ```pipenv install```.

### 3.1 Introduction to Vector Search
- [Video](https://youtu.be/C5AWdL3kg1Q?si=yo7wtHA4DGxzivgG) and [slides](https://github.com/dataML007/elastic_search/blob/main/Introduction%20to%20Vector%20DB.pdf).
In a nutshell, 
1. The meaning of texts are dependent on the surrounding context. Example, "Apple" could represent a company or a fruit. Hence to preserve this semantic meaning, these words are converted into vector embeddings (numeric) which represent the semantic meaning in a high-dimensional vector space. 
2. This vector space allows different words with similar semantic meanings to be close to each other in this space, while different meanings would be further apart.
3. The vector space a.k.a a vector database is also advantageous as vector information are stored in an optimal way compared to storing plain text, and much faster for information retrieval.
4. How are vector embeddings created? To train a model for encoding texts into embeddings, large amounts of data are first collected, models are pretrained to generate embeddings from collected data, and then embeddings are evaluated, and finally the best model is selected.
5. In LLM, you have an information vector DB and queries are first encoded with the same embedding model into vector embeddings. Then similarity scoring metrics such as Cosine-Similarity, Dot Product, Euclidean Distance are applied to find the best response within the vector DB for the encoded queries. 
- Also read [What is a vector database?](https://www.elastic.co/what-is/vector-database).

### 3.2 Semantic Search with Elastic Search
- <b>Goal</b>: Convert the FAQ document into vector embeddings and index into ElasticSearch DB.
- Bring up ElasticSearch container with Docker:
```
docker run -it \
    --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
```
- Install [Sentence Transformers](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html): ```pipenv install sentence_transformers==2.7.0```.
- Refer to code block at [Pretrained Models](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html#pretrained-models) to embed sentences with Sentence Transformer models.
- Selected fields from the preprocessed document are embedded with a pretrained model and added into the ElasticSearch index.
- The query is also embedded with the same pretrained model.
- ElasticSearch search is done using KNN to perform vector search.

### References
1. https://logz.io/blog/elasticsearch-mapping/#:~:text=Within%20a%20search%20engine%2C%20mapping,indexes%20and%20stores%20its%20fields

2. https://www.sbert.net/docs/sentence_transformer/pretrained_models.html

3. https://www.elastic.co/search-labs/tutorials

4. https://www.elastic.co/search-labs/blog/text-similarity-search-with-vectors-in-elasticsearch