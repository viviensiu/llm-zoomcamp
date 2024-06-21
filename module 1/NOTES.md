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