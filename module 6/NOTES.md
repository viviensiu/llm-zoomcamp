## Module 6: Best practices
All module 6 videos and notebook links can be found [here](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/06-best-practices/README.md)

### 6.1 Techniques to Improve RAG Pipeline
Recap of key concepts in a RAG system:
* Indexing stage:
    * Parse initial documents.
    * Chunking: Split texts into chunks or paragraphs.
    * Embed each chunk into vector.
    * Store the vectors into DB.
* Answering stage:
    * Turn user question into vector form.
    * From the DB, retrieve top K documents relevant to the question.
    * Augment the question prompt with context (top K documents) and pass it to LLM.
    * LLM returns the answer.

**Techniques to improve RAG pipeline**:
* **Small-to-big chunk**:
    * Problem of choosing the right chunk size as: Large chunk sizes may generate too much noise in the embeddings and cause the information retrieval step to perform poorly since we're unable to retrieve the relevant info due to noise. Small chunk size may cause the retrieved context to be incomplete, therefore causing incomplete responses by the LLM.
    * To mitigate this, apply small chunk size strategy in indexing stage, e.g. only a whole sentence as a chunk. And then use a large chunk size at answering stage by combining several relevant chunks as context.
* **Leveraging document metadata**:
    * Adding metadata (such as date, title) can be useful as additional information, which could then be used for topic modeling (NLP technique to summarise text data through word groups).
    * We could also ask LLM to extract attributes characterising our document.
* **Hybrid search**:
    * Combine vector-based (semantic search) and keyword-based search (lexical search).
* **User query rewriting**:
    * Reformulate queries using a separate LLM to remove noise and improve its structure, before performing retrieval.
* **Document reranking**:
    * Documents with the highest embedding similarity may not be most relevant.
    * Hence, an option is to rerank the retrieved document chunks, e.g. using LLM, and then use the top reranked chunks as context for the LLM.
* **References**:
    * [Five Techniques for Improving RAG Chatbots - Nikita Kozodoi](https://www.youtube.com/watch?v=xPYmClWk5O8).

### 6.2 Hybrid search
* Uses a combination of vector-based search and keyword-based search to produce results.
* Hybrid Search is ranked using hybrid_score $= (1-\alpha) *$ match_score + $\alpha *$ vec_score, where $\alpha \in [0,1]$.
* We will use notebooks from module 3 to cover vector search and its evaluation method in the hybrid search.
* We will also refer to [Elasticsearch guidelines to setup hybrid search](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html#_combine_approximate_knn_with_other_features).
* [Elasticsearch Hybrid Search tutorial: Combined Full-Text and kNN Results](https://www.elastic.co/search-labs/tutorials/search-tutorial/vector-search/hybrid-search).
* Start Elasticsearch container first:
```bash
docker run -it \
    --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
```
* Steps:
    * Modify the ES search functions to use hybrid search.
    * Run hybrid search on ground truth data and evaluate using Hit Rate and Mean Reciprocal Rank.
    * Compare hybrid search evaluation results with Module 3's vector search evaluation results.

### 6.3 Document Reranking
* Document reranking works by scoring and reranking the retrieved document chunks from index to improve its relevancy related to the user query.
* Typically done at the last step of retrieval before passing the search results from knowledge base to LLM, as reranking millions of documents in knowledge base would be highly inefficient.
* There are multiple techniques for this, for example simply heuristic implementation and using specific models to rerank the chunks.
* In this lesson we will call the LLM twice:
    * Ask the LLM to rerank our chunks.
    * Ask the LLM to use the context (from reranked chunks) to generate the response back to user.
* Naturally the relevance scores should be evaluated based on some metrics, e.g.:
    * [NDCG](https://www.evidentlyai.com/ranking-metrics/ndcg-metric#:~:text=Normalized%20Discounted%20Cumulative%20Gain%20(NDCG)%20is%20a%20ranking%20quality%20metric,DCG%20representing%20a%20perfect%20ranking.).
    * [MAP@K](https://www.evidentlyai.com/ranking-metrics/mean-average-precision-map).
    * Reciprocal Rank Fusion (RRF).
    * etc.
* The reason why cosine similarity is not used here is because of we're using hybrid search instead of just vector search, therefore we will apply Reciprocal Rank Fusion (RRF) metrics to our reranking strategy.
* Elasticsearch has a built-in RRF within the search query. See here on ["How RRF works"](https://www.elastic.co/search-labs/tutorials/search-tutorial/vector-search/hybrid-search#how-rrf-works). 
* **Note**: The RRF feature is only available in Platinum/Enterprise version of Elasticsearch ([subscription](https://www.elastic.co/subscriptions) required), from version 8.9 and later. If you have this version, you will need to switch to use the following ES container instead:
```bash
docker run -it \
    --rm \
    --name elasticsearch \
    -m 4GB \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.9.0
```
* **Note**: It is also possible to integrate external reranking models such as [Cohere's Rerank 3 model](https://www.elastic.co/search-labs/blog/elasticsearch-cohere-rerank) but for this module we will stick to something simple.
* Also read [Elasticsearch's Reciprocal rank fusion guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html) and [RRF research paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf).
* Steps for own implementation of RRF metric:
    * The ES search results are already ranked from most to least relevant.
    * For the list of results, assign ranking constant $k$ of each result using enumerate() and calculate score using this formula:
        <br>score $+= 1.0 / ( k + \text{rank}( \text{result(q)}, d ) )$
    * Note that score is incremented for results coming from same document $d$.
    * Rerank all results based on their scores and return the top $n$ results.
