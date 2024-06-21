## Setup environment with pipenv, elasticsearch
- ```conda create -n llm-zoomcamp-env python```
- ```conda activate llm-zoomcamp-env```
- ```conda install pip```
- ```pip install pipenv```
- ```pipenv install tqdm notebook==7.1.2 openai elasticsearch```
- ```pipenv run jupyter notebook```
- Install Docker and execute in terminal 
```
docker run -it \
    --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
```
- Check if elastic search setup is successful: ```curl http://localhost:9200```

## Optional setup to use HuggingFace with LangChain instead of OpenAI
- ```pipenv install "langchain[all]"```
- ```pipenv install python-dotenv```
- ```pipenv install langchain-huggingface```

## Get HuggingFace API key
Register HuggingFace API key, see [here](https://youtu.be/jo_fTD2H4xA?si=tQ3l77ucRzaVwa6D) for guideline.

## .env
- Create a .env file containing ```HF_KEY=<Your HuggingFace API key>```