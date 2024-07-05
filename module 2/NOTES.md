## Module 2: Open-Source LLMs
All module 2 videos and notebook links can be found [here](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/02-open-source). All module 2 notebooks are executed in existing conda environment ```llm-zoomcamp-env``` with ```pipenv install```.

### 2.1 Introduction
Motivation: Replacing OpenAI in Module 1 with open-source LLM

### 2.2 Using SaturnCloud for GPU Notebooks
- <b>Goal</b>: Setup [SaturnCloud](https://saturncloud.io/) account to have GPU access to run open-source LLM.
- <s>[Closed on 25th June 2024] Register for an account with free GPU access at LLM Zoomcamp website.</s>
- Log on to Saturn Cloud and setup the following:
    1. ```Secrets```: Store your API keys for various open-source LLMs here (e.g. HuggingFace API key)
    2. ```User``` -> ```Manage <user name>``` -> ```Git SSH Key```: click on ```Create SSH key```. Then paste this SSH key to your Github SSH Public Key (under your Github profile -> Settings -> SSH and GPG Keys -> click on "New SSH Key" and copy-paste in "Key") to allow access from your SaturnCloud to your Github. Also see [Official guide](https://saturncloud.io/docs/using-saturn-cloud/gitrepo/?_gl=1*1tevkte*_gcl_au*OTgyMTk1MjUuMTcxOTI1ODQ5OC4xNzg2ODQyMDY1LjE3MTkzOTU0MzIuMTcxOTM5NTQ1Mg..*_ga*MTI1OTcxODE1NC4xNzE5MjU4NDk4*_ga_9QKGCS5Q41*MTcxOTQwNzAzMC41LjAuMTcxOTQwNzAzMC42MC4wLjA.#set-up-git-ssh-keys).
    3. ```Resources```: click on ```New Python Server``` 
        - ```Overview```: fill in notebook name.
        - ```Hardware```: select "GPU", Size: select "T4 XLarge - 4 cores - 16GiRAM - 1 GPU".
        - ```Environment``` -> ```Image```: "saturncloud/saturn-python-llm".
        - ```Extra packages``` -> ```Pip```: ```pip install -U transformers accelerate bitsandbytes```
        - ```Git repositores```: copy-paste the SSH path of your personal Git repo created for this module. Path should look like "git@github.com..............git".
        - Finally, click "Create" to create the new Jupyter server.
    4. Once the Jupyter server is created, go to ```Secrets and Roles``` tab. Click on ```Attach Secret Environment Variable``` and select the API key which was previously setup in Step 1.
    5.  Go to ```Overview``` tab and click "Start" to start the server.
    6. Once the server is up, click on ```Jupyter Notebook``` to start the notebook.
    7. [Optional] If you're accessing source codes from Github repo, under the Jupyter Server that was created, set ```Git Repos``` -> ```Restart Behavior``` to reclone to automatically fetch the latest updates in your Git repo upon restart. Note that changes made in SaturnCloud is not pushed to your Github.
    8. You can always find your created servers in Saturn Cloud under ```Resources```. Scroll down to find them.

### 2.3 HuggingFace and Google FLAN T5
- <b>Goal</b>: replace the OpenAI model with the FLAN-T5-XL model.
- Create [starter notebook](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/02-open-source/starter.ipynb) locally.
- Link to [HuggingFace FLAN-T5 XL model page](https://huggingface.co/google/flan-t5-xl)
- Link to [HuggingFace FLAN-T5 documentation](https://huggingface.co/docs/transformers/en/model_doc/flan-t5)
- Link to [T5's documentation page](https://huggingface.co/docs/transformers/en/model_doc/t5)
- Update env. variable HF_HOME to use a directory with larger storage inside notebook.
- Refer to the code block under [Running the model on a GPU](https://huggingface.co/google/flan-t5-xl#running-the-model-on-a-gpu) for subsequent steps.
- Import the tokenizer and FLAN-T5-XL model.
- Modify the llm() to do:
    1. Format the prompt with query and context.
    2. Encode prompt with tokenizer.
    3. FLAN-T5-XL model will generate a encoded response from the encoded prompt.
    4. Decode the response back into plain text.

### 2.4 Phi 3 Mini
- <b>Goal</b>: replace the OpenAI model with the Phi3 model.
- Duplicate the notebook built in 2.3 and modify from there. This helps to retain the env variables setup done previously.
- Link to [HuggingFace Microsoft Phi3 model page](https://huggingface.co/microsoft/Phi-3-mini-128k-instruct)
- Link to [Huggingface pipeline doc page on text generation](https://huggingface.co/docs/transformers/main/en/main_classes/pipelines#transformers.TextGenerationPipeline)
- Refer to the code block under [Sample Inference Code: This code snippets show how to get quickly started with running the model on a GPU](https://huggingface.co/microsoft/Phi-3-mini-128k-instruct#sample-inference-code) for subsequent steps.
- Import the tokenizer and Phi3 model.
- Modify the llm() to do:
    1. Format the prompt with query and context.
    2. Encode prompt with tokenizer.
    3. Phi3 model will generate a encoded response from the encoded prompt.
    4. Decode the response back into plain text.

### 2.5 Mistral-7B and HuggingFace Hub Authentication
- <b>Goal</b>: replace the OpenAI model with the Mistral-7B model.
- Duplicate the notebook built in 2.4 and modify from there. 
- Link to [HuggingFace Mistral-7B model page](https://huggingface.co/mistralai/Mistral-7B-v0.1)
- To use this model, you must: 
    1. Accept the agreement in the [model page](https://huggingface.co/mistralai/Mistral-7B-v0.1).
    2. Setup a HuggingFace account. Under ```Settings``` -> ```Access Tokens```, create a new token, copy the token (should begin with ```hf_************```)
    3. [Optional] Add this to your SaturnCloud account list of secret keys. See Section 2.2 notes under Step 4.
    4. If you skip Step 3, you'll need to find a way to import this HuggingFace token into the code, e.g. by hardcoding.
- The sample code block for Mistral-7B is taken from [HuggingFace LLM Tutorial](https://huggingface.co/docs/transformers/en/llm_tutorial)
- Load the HuggingFace token in your code. If you have done Step 3 above, the ```os.environ``` key must match the name of the env. variable that was set as per Step 3 above.
- Import the tokenizer and Mistral-7B model.
- Modify the llm() to do:
    1. Format the prompt with query and context.
    2. Encode prompt with tokenizer.
    3. Mistral-7B model will generate a encoded response from the encoded prompt.
    4. Decode the response back into plain text.
- <b>Note</b>: This model requires authentication and may pose an issue if we want to put it in a container. The other option would be to download the model, save and load it locally so you can skip the authentication. See the note ["Using Mistral-7B Model in Production"](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/02-open-source/serving-hugging-face-models.md) for detailed instructions.

### 2.6 Exploring Open Source LLMs
Basically to explore various open-source models on HuggingFace, you could adopt a "plug-and-play" method by referring to the codes found in model pages.
Other open-source models:
- [LLM360/Amber](https://huggingface.co/LLM360/Amber)
- [Gemma-7B](https://huggingface.co/blog/gemma)
- [SaulLM-7B](https://huggingface.co/papers/2403.03883)
- [Granite-7B](https://huggingface.co/ibm-granite/granite-7b-base)
- [MPT-7B](https://huggingface.co/mosaicml/mpt-7b)
- [OpenLLaMA-7B](https://huggingface.co/openlm-research/open_llama_7b)

<b>Note</b>: Check how many parameters the models are using to know if the GPU can handle them. For SaturnCloud, 1 GPU could handle models with <=7B parameters. 

Another attribute to look out for is the quantization parameter used in the model, specified under ```Experiment``` in [Open LLM Performance Leaderboard](https://huggingface.co/spaces/optimum/llm-perf-leaderboard), e.g. 4bit, 16bit. Implication: Faster but less precise model. 

Good places to start for finding good open-source LLMs:
1. Leaderboards. Example: [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) and [Open LLM Performance Leaderboard](https://huggingface.co/spaces/optimum/llm-perf-leaderboard)
2. Google
3. ChatGPT

### 2.7 Running LLMs Locally without a GPU with Ollama
Ollama - allow LLMs to run on a CPU. To begin, refer the official guide at [Ollama Github README](https://github.com/ollama/ollama).

Setup guide:
1. [Download Ollama](https://ollama.com/download). For Mac users, double-click on the downloaded Ollama application and follow the instructions. [Guide](https://medium.com/free-or-open-source-software/ollama-get-up-and-running-with-llama-2-mistral-and-other-large-language-models-on-macos-4c5b8d404acc).
2. Test installation in terminal: input ```ollama run phi3```
3. Test with a general question: ```I just discovered the course. How do I join```
4. Test with a [prompt](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/02-open-source/prompt.md)
5. Input ```/bye``` to exit from Ollama in terminal.

- <b>Goal</b>: replace the OpenAI model with the Ollama model.
- Duplicate the notebook built in 2.4 and modify from there. 
- Modify the llm() to use phi3 model.
- Modify the OpenAI client object to use Ollama as below:
```
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',
)
```
Alternative to installing Ollama on your local machine: Running Ollama with Docker.
1. In terminal, input:
```
docker run -it \
    -v ollama:/root/.ollama \
    -p 11434:11434 \
    --name ollama \
    ollama/ollama
```
2. Open a new terminal and input ```docker exec -it ollama bash``` to enter the ```ollama``` container and execute an interactive bash , then ```ollama pull phi3``` to pull the phi3 model into this container.
3. Once Step 2 is done, execute your jupyter notebook as usual.

### 2.8 Ollama + Elastic in Docker Compose
- <b>Goal</b>: rerun notebook from Module 1 with local LLM using Ollama.
- Create a docker-compose.yaml file to pull images and run ollama and elasticsearch containers:
```
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.4.3
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
      - "9300:9300"
  ollama:
    image: ollama/ollama
    container_name: ollama
    volumes:
      - ollama:/root/.ollama
    ports:
      - "11434:11434"
volumes:
  ollama:
```
- In a new terminal, execute ```docker-compose up```.
- In a new terminal and input ```docker exec -it ollama bash```, then ```ollama pull phi3```.
- Copy-paste the rag notebook from Module 1 into Module 2. Rename as rag-ollama. 
- Modify the following:
    - Remove minsearch codes.
    - Modify OpenAI codes with the Ollama codes used in Section 2.7.
- Execute ```docker-compose down``` to stop and remove containers once finished with experiments.

### 2.9 Creating a Streamlit UI
- <b>Goal</b>: To create a Streamlit UI to allow user interaction with the RAG-Ollama
- Execute ```pipenv install streamlit``` in the virtual env ```llm-zoomcamp-env```.
- From the rag-ollama notebook created in Section 2.8, copy-paste the following:
    - OpenAI client and ElasticSearch client.
    - functions elastic_search(), build_prompt(), llm(), rag().
- Define a main function for the Streamlit UI that incorporates:
    - a text input field and a button to submit the user input to rag().
    - a spinner to indicate processing.
    - an output to display the response from rag().
- <b>Extra</b>: Create a class that creates an ElasticSearch index "course-questions" if none exists. See ```elasticSearchRag.py```.
- Check if Ollama and ElasticSearch containers are running by executing in terminal ```docker ps```.
- If Ollama and ElasticSearch containers are not running, execute ```docker-compose up``` to bring up Ollama and ElasticSearch.
- Execute ```pipenv run streamlit run "module 2/qa_faq.py"```
- Test the Streamlit UI with the question ```I just discovered your course. Can I still join?```
- Sample UI with output:
![Alt text](../img/rag_streamlit.png?raw=true "Title")
- Other options for UI: Flask, Telegram, etc.

### Using Google Colab GPU
- <b>Goal</b>: Run open-source LLM (Google FLAN-T5 XL) with Google Colab GPU
- [Video link](https://www.loom.com/share/591f39e4e231486bbfc3fbd316ec03c5)
- Duplicate the flan-t5 notebook created at Section 2.3.
- Ensure ```Runtime type``` is set to ```T4 GPU``` in Colab.
- Include the ```!pip install -U transformers accelerate bitsandbytes``` commands within the notebook.
- <b>Note</b> that there is no need to change the ```HF_HOME``` env. variable to point to /run/cache when using Google Colab as the storage are all temporary anyway.
- Execute notebook in Colab as usual.

### Homework
- Link to [homework questions](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2024/02-open-source/homework.md).

### Other notes
- To check which type of GPU is used in Saturn Cloud: After starting Jupyter Notebook, click on "New" -> "Terminal". Type in ```nvidia-smi```.
- To watch your GPU usage, in the same terminal window, type in ```watch nvidia-smi```
