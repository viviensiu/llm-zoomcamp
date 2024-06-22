## Module 1: Introduction

### 1.1 Intro. to LLM and RAG
- RAG: Retrieval Augmented Generation
- In a chatbot application with RAG, a user query is packaged together with the information retrieved from a knowledge base and sent to an LLM, which will utilise the retrieved information as additional context, in order to provide a relevant response to the user query. 
- Retrieval: Refers to the information retrieval from knowledge base.
- Augmented: The prompt (user query) is augmented with the retrieved info for context.
- Generation: The response from LLM.

### 1.2 Environment Preparation
- Install Docker
- run ```pip install tqdm scikit-learn openai notebook==7.1.2 elasticsearch pandas```
- register for an OpenAI API key at [OpenAI](https://platform.openai.com/docs/), alternatively use an open-source.
- in terminal, run ```export OPENAI_API_KEY="\<your api key here\>"```
- start jupyter notebook in terminal: ```jupyter notebook```. If it asks for token, copy-paste the token found in terminal.

Alternatively to reuse the Pipfile established from "pre-course workshop 1", do the following:
1. conda activate the virtual env with pipenv installed, in this case I use my virtual env. "llm-zoomcamp-env" which was setup since the pre-course workshop 1.
2. run ```pipenv install``` to install all packages specified in Pipfile.
3. run ```pipenv install pandas scikit-learn```
3. run ```pipenv run jupyter notebook``` to bring up jupyter notebook.

### 1.3 Retrieval and Search
- Goal: Build an indexed knowledge base using data from a JSON file which contains FAQ on data engineering zoomcamp, and use this to return relevant search results to user queries.
- elasticsearch is built-in from the course-provided Python file minsearch.py. 
- Use minsearch.Index to create an index object where keyword_fields is similar to sql query filter condition. text_fields are for performance search.
- the index object is then fitted with the FAQ data. 
- During search, fields such as "question" and "section" weights are modified with boost to emphasize their relative importance when used to retrieve search results based on queries. The filter can be specified as well to limit search on certain courses only.
- Query using index.search() together with the boost modifications and return top 5 results.

### 1.4 Generating Answers with OpenAI GPT-4o
- Goal: Send context from documents to LLM to generate more accurate response.
- Create a prompt template to accept dynamic query and context before sending to the LLM. Also limits the type of responses LLM can provide.
- Create context based on the query's search results from index.
- Modify the prompt template based on the context to create the prompt .
- Supply the prompt to LLM and generate a response.

### 1.4.2 Exploring alternatives to OpenAI
A list available [here](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/open-ai-alternatives.md)

### 1.5 The RAG Flow Cleaning and Modularizing Code
- Goal: Clean up and modularise the codes created from earlier sections.
- search(): Perform a query using index.search() and returns top results.
- build_prompt(): creates a dynamic prompt template which accepts query and context built from search() result to return a prompt.
- llm(): returns a LLM response based on prompt.
- rag(): accepts a query, go through flow search() -> build_prompt() -> llm() and provides an answer to the query.

### 1.6 Replace minsearch with ElasticSearch
- Goal: replace search() with elastic search
- Pros: elasticsearch is persistent, while minsearch knowledge base is deleted when notebook shutdown.
- run the following if elasticsearch is not setup yet:
```
docker run -it \
    --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
```
- test that elasticsearch db is connected using "localhost:9200"
- create the ES indices. Specify index name, index setting (mapping properties which map to the FAQ document fields, and the search keyword which is the "course" field in FAQ document).
- create the ES index by indexing each row of document text in documents. Progress is tracked by tqdm.
- elastic_search(): Based on a query, filter to only search the ES index in course=data-engineering-zoomcamp, then retrieve the top 5 results that  closely match the fields "question", "text", "section". Notice that question has been given thrice the weights.
- modify the rag() by replacing search() with elastic_search().