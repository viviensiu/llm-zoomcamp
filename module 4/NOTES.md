## Module 4: Evaluation and Monitoring
All module 4 videos and notebook links can be found [here](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/04-monitoring/README.md).

**Note**: I completed this module using the ```llm-zoomcamp-env``` virtual env as per previous modules.

**Evaluation**: Assess the quality of our entire RAG system before it goes live.

**Monitoring**: Collect, store and visualize metrics to assess the answer quality of a deployed LLM. Also collect chat history and user feedback.

### 4.1 Introduction to monitoring answer quality
**Why monitor the answer quality of LLM systems?** 
Monitoring the system helps us to ensure that the system is working as intended. There are past scenarios where the LLM systems from Microsoft, Google which performed badly (biased), which affected the company's reputation and trust in public.

**Steps to monitor answer quality of LLMs**
1. Compute different types of quality matrics:
    - Vector similarity between expected/ground truth and LLM answers.
    - LLM-as-a-judge to compute toxicity of LLM answer.
    - LLM-as-a-judge to assess quality of LLM answer.
2. Store computed metrics in relational databases e.g. PostgreSQL.
3. Use Grafana to visualize metrics over time.
4. Store chat sessions and collect user feedback in database, this helps to pinpoint areas of improvement for the system.
5. Use Grafana to visualize user feedback and corresponding chat sessions.

**What else to monitor, and things not covered in this module**
- Further quality metrics and user feedback, i.e. bias and fairness, topic clustering, textual user feedback.
- System metrics: Latency, Traffic, Errors, Saturation.
    - Latency: How long it takes to receive a response.
    - Traffic: Num. of users using the chatbot.
    - Errors: Does system respond with error code.
    - Saturation: Resource consumption of the system, e.g. memory, GPU.
- Cost of used infrastructure, e.g. cost of vector store, LLM API calls.

### 4.2 Offline vs Online (RAG) evaluation
Recall that back in RAG modules, we created a RAG application with the following steps:
- Retrieve relevant information based on user query as context.
- Augment the prompt with the retrieved context and feed this to LLM.
- Generate the response from LLM back to user.
We also evaluated our search results in retrieval using:
- Hit Rate.
- Mean Reciprocal Rank (MRR).
Now, to evaluate the whole LLM application, there are 2 ways:
- **Offline evaluation**: Done **before** deployment, e.g. with Hit Rate and MRR, smilarity measures (cosine similarity) between ground-truth data and LLM response like in Module 3, LLM-as-a-judge (using another LLM to evaluate responses from one LLM).
- **Online evaluation**: A/B tests, experiments, user feedback.
Monitoring is done to observe the overall health of the system:
- Performance metrics, e.g. LLM response quality.

### 4.3 Generating data for offline RAG evaluation
**Goal** Given some questions, evaluate LLM responses (answers) for a Q&A chatbot with ground-truth data (original answers). This helps to evaluate if a chosen LLM's performance meets our expectations in development environment before it's used as the LLM in a production setting.
**Setup**:
- Execute ```pipenv install seaborn```
- Bring up Elastic Search container with ```docker start elasticsearch``` or 
```bash
docker run -it \
    --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
```
- Load the documents with ids and ground-truth data.
- Load a Sentence Transformer embedding model to generate vector embeddings.
- Setup ES index with vector embeddings on question and text, vector search function to retrieve answers based on cosine similarity.
- Setup ES Search with KNN to retrieve top 5 results of the vector search.
- Setup RAG flow that retrieves 5 ES Search results, augment the prompt with search results, and generate a response using OpenAI API.
- For the LLM comparison, I will be comparing Llama2-7B, Llama3-8B and (maybe) Llama3.1-8B. Hence the prequisites are:
    - [Download and install Ollama](https://ollama.com/download).
    - Bring up Ollama service in local computer.
    - Execute in terminal: ```ollama pull llama2:7b```, ```ollama pull llama3:8b```, ```ollama pull llama3.1:8b```. 
    - **NOTE**: Refer to [Ollama library](https://ollama.com/library) for the correct model names and tags.
**Prepare data for evaluation**
- Given a ground-truth question and answer pair, the same question is fed to RAG to generate a response.
- For Module 4.3, we evaluate LLM models GPT-4o and GPT-3.5 Turbo, I changed it to Llama2-7B, Llama3-8B.
    - Llama2-7B response generation took 5 hours.
    - Llama3-8B response generation (with parallelization using [ThreadPoolExecutor](https://medium.com/@rajputgajanan50/how-to-use-threadpoolexecutor-in-python-3-6819c7896e89)) took 3.1 hours.
- The generated answers together with the ground-truth are saved in CSVs for further evaluation in Module 4.4.

### 4.4 Offline RAG evaluation: cosine similarity
(Same notebook as 4.3)

**Evaluation**:
- Load the saved CSVs from Module 4.3.
- Generate vector embeddings for LLM response and ground-truth answer. 
- The response is then compared to the answer in ground-truth to evaluate how similar they are. This is done by computing the cosine similarity between both vector embeddings. 
- A result close to 1 means highly similar, and vice-verse if the result is close to 0.
- We could also evaluate based on the cosine similarity statistics and distribution, e.g. mean, median, to compare the candidate LLMs. 
- The cosine similarity could also be plotted for comparison. 

**NOTE** I skipped evaluation on Llama3.1-8B as it was incredibly slow on Ollama.

### 4.5 LLM-as-a-judge
(Same notebook as 4.3)
- Alternative to using cosine similarity, we could use another LLM (different than the one used for chatbot) to evaluate whether the response is relevant to the original question and/or original answer.
- In a online RAG evaluation setting, we will not have access to the original/expected answer, this prevents cosine similarity to be carried out.
- However, this is not an issue with LLM-as-a-judge despite the lack of original answer, hence it is a convenient method to perform evaluation on the fly.
- **Method**:
    1. Create a prompt that instructs the LLM to have an evaluator persona, accepts the responses and original data, specify how the evaluation metric works and the JSON format of the evaluation results. Example of evaluation metric: classify as "RELEVANT", "PARTLY RELEVANT", "NON RELEVANT"
    2. Extract a random set of samples from the saved CSVs in Module 4.3, e.g. 150 samples.
    3. For each sample, parse the information into LLM and retrieve the evaluation results.
    4. Examine the distribution of relevance classes.
    5. Look at the responses and original answers of selected negative records (LLM responses classified as "NON RELEVANT") to see where the issue may be at.

### 4.6 Capturing User Feedback
**Goal**: 
- To capture user satisfaction with the LLM response. Given a user query, an LLM response and a user feedback (thumbs up, thumbs down), these information will be stored in PostgreSQL.
- Containerize the chatbot app using a docker-compose file that would:
    - Persist data in Elastic Search index to prevent reindexing data on every run.
    - Include PostgreSQL with volume mapping.
    - Include a separate container for the Streamlit app.
- The source codes in this module are generated using Claude-Sonnet!

**New Packages**
-  psycopg2-binary: PostgreSQL database adapter for the Python programming language.

**Setup**
- Install pgcli to be able to run SQL queries in PostgreSQL via CLI.
```bash
pip install pgcli
pgcli -h localhost -U your_username -d course_assistant -W
```
- .env: Stores env variables for PostgreSQL, Elastic Search, Ollama, Streamlit, embedding model and index name.
- Dockerfile: customise the docker image for the Streamlit chatbot.
- docker-compose.yml: contains configurations to build multiple Docker containers.
- requirements.txt: contains list of packages required for the Streamlit chatbot.

**Initialization**
* One-time execution of ```prep.py```
* Run ```docker-compose up```, which will:
    - Initialise the required containers: elasticsearch, ollama, postgres, grafana.
    - Build an image based on Dockerfile.
    - Create a Docker container for the Streamlit chatbot, and install required Python packages listed in requirements.txt.

**Chatbot Modules**
- prep.py: One-time initialization to setup Elastic Search index.
- assistant.py: RAG assistant to accept a user query, performs vector search in ES Index for context, and returns an LLM response based on the context.
- db.py: initialise connection, retrieve, save conversations and feedbacks to PostgreSQL DB.
- app.py: the streamlit app for the chatbot.

**Debugging**
- Use ```pgcli``` to check PostgreSQL tables.
- ```pip freeze > <some txt file>``` provides the full list of all packages in the current env.
- To rebuild images in docker-compose, execute ```docker-compose stop <service>``` and then ```docker-compose build <service>```.

### 4.6.2 Capturing User Feedback, Part 2
**Goal**
- Option to toggle between text search or vector search.
- Option to toggle between using Ollama or GPT.

**Approach**
- Update app.py to offer those options.

### 4.7 Monitoring the System using Grafana
**Goal**
- Monitor the LLM chatbot in terms of input tokens, completion tokens, costs, user feedback etc. in a Grafana dashboard that connects to Postgres at the backend.
- As per 4.6, the source codes are generated using Claude-Sonnet by prompting on the responses we want in monitoring with Grafana!

**Approach**
- Implement changes in app.py
- Rerun ```prep.py``` to recreate the database with new schema.
- Reexport postgres host: ```export POSTGRES_HOST=localhost```.
- Rebuild streamlit service inside docker-compose with ```docker-compose build streamlit```
- Perform healthcheck on Streamlit in web browser: ```localhost:8501``` and submit a few questions to test out the logging.
- Access Grafana via ```localhost:3000``` and login with ```admin/admin``` for user name and password.
- Setup data source for ```Postgres``` in Grafana (refer ```.env``` for Postgres settings below):
    - Host: ```postgres```.
    - Database name: ```course_assistant```.
    - User: ```your_username```.
    - Password: ```your_password```.
    - Click ```Save & Test```.
- Run ```python generate_data.py``` to generate some synthetic data for Grafana dashboard simulation.
- In Grafana, click on ```Add Panel``` to begin adding panels. You could customise the panel by inserting the SQL query you want to run for this panel, which will filter and display the results from the database specified above.
- The SQL queries used for the chatbot Grafana dashboard can be referred to at **grafana.md**.

### 4.7.2 Extra Grafana Video
- Walks through how Grafana panels can be customized in WHERE statement to include special Grafana variables for filtering start/end periods, see **grafana.md**. 
- To save and load Grafana dashboard: Click on the ```Settings icon``` in dashboard, go to ```JSON Model```, copy-paste the JSON code into a local file and save locally.
- Sharing Grafana dashboard: Click on ```Share icon```, click on ```Export``` and ```Save to file```.
- Load Grafana dashboard from a saved file: Click on ```Dashboard icon``` on the left panel --> ```Import``` --> Click on ```Upload JSON file```.

### Ollama running on Mac
[Apple Silicon GPUs, Docker and Ollama: Pick two.](https://chariotsolutions.com/blog/post/apple-silicon-gpus-docker-and-ollama-pick-two/)

