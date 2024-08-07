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

### 3.3 Evaluating Retrieval
See [eval repo](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/03-vector-search/eval) for all course notebooks and files.

### 3.3.1 Evaluation Metrics for Retrieval
- Goal: To understand how to evaluate the retrieval methods used in previous modules, e.g. minsearch, ElasticSearch.
- The retrieval method influences the quality of the response.
- Given a query, you can set some standards where you expect the responses to come from. Example:
    Query: "I just discovered your course, can I still join?"
    Expected best response: retrieve most relevant results from doc1, doc10, doc11.
    If the responses are close to expectations, the performance is good, else otherwise.
- Hence the following approaches are used for evaluation:
    1. Ground truth / gold standard data.
    2. Human feedback on generated responses, typically one could sample ground truth from production data. However if non-available, ground truth data can be generated from LLM.
    3. Evaluate the retrieval results based on ground truth.
- In the previous module, we have seen the way ElasticSearch is configured to retrieve results based on a query. Some fields are given a boost, some fields are left out. There are many ways to configure these search criterias or to embed these data, note that there is no universal standard of a "best" method, as this typically depends on data characteristics.
- Typically, the relevancy of search results are ranked. Here are some [common ranking evaluation metrics](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/03-vector-search/eval/evaluation-metrics.md).

### 3.3.2 Ground Truth Dataset Generation for Retrieval Evaluation
- <b>Goal</b>: For each record in the FAQ document, generate 5 questions using LLM. These questions-record pairs will serve as the gold standard/ground truth dataset to evaluate retrieval methods in subsequent lessons.
- <b>Note</b>: As there are no production system nor domain experts for human feedback, we resort to using LLM for such generation.
- Steps:
    1. For each record, generate a unique ID so the generated questions could be linked to the original record.
    2. Cross-check if the IDs are unique per document.
    3. Save the results from above into new file.
    4. Generate the questions for each record using LLM.
    5. Parse the questions in JSON format and save into CSV.
- <b>Note</b>: Ollama with Phi3 model instead of GPT-4o is being used to generate questions, which took 7H 17m. To start Ollama, I used the docker-compose file that was created in Section 2.8 to start the Ollama container. Alternatively, download the results.bin file from the LLM-zoomcamp module 3 repo to skip the LLM question generation step and parse questions in JSON format directly and save as CSV.

### 3.3.3 Ranking evaluation: text search
- <b>Goal</b>: Evaluate the text search retrieval results using ground-truth data with Hit Rate (HR) and Mean Reciprocal Rank (MRR).
- Setup:
    - Copy minsearch.py from Module 2 into Module 3 folder.
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
- Steps:
    1. Create an ElasticSearch index using documents-with-ids.json and an ES Search to perform text search in this index.
    2. Loop thru all ground-truth questions and use them to perform ES Search. For each question, retrieve the IDs from search result and compare with the IDs tied to this question in ground-truth data. If the IDs match, set it to True, else False.
    3. Evaluate the comparison results using Hit Rate and MRR.
    4. Repeat Steps 1 to 3 by replacing ES Search with MinSearch.

### 3.3.4 Ranking evaluation: vector search
- <b>Goal</b>: Evaluate the vector search retrieval results using ground-truth data with Hit Rate (HR) and Mean Reciprocal Rank (MRR).
- 3 different methods to evaluate:
    * Embedding on questions only.
    * Embedding on answers only.
    * Embedding on questions and answers.
- The sentence embedding model is selected from [Sentence Transformers](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html). Unlike in Section 3.2, a smaller embedding model is used instead to reduce time.
- Bring up ElasticSearch container with Docker as per Section 3.3.3 or if the container is not removed yet, execute ```docker start elasticsearch```.
- Steps:
    1. Create an ElasticSearch index using documents-with-ids.json and an ES Search which has the questions, answers embedded (individualy and combined) to perform vector search (using KNN) in this index.
    2. For each method to be evaluated:
        - Loop thru all ground-truth questions, embed the ground-truth questions, specify the index field that is relevant to the method and perform ES search.
        - Evaluate the search results using Hit Rate and MRR.

### Homework
- Link to [homework questions](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2024/03-vector-search/homework.md).

### References
1. https://logz.io/blog/elasticsearch-mapping/#:~:text=Within%20a%20search%20engine%2C%20mapping,indexes%20and%20stores%20its%20fields

2. https://www.sbert.net/docs/sentence_transformer/pretrained_models.html

3. https://www.elastic.co/search-labs/tutorials

4. https://www.elastic.co/search-labs/blog/text-similarity-search-with-vectors-in-elasticsearch