## Module 4: Evaluation and Monitoring
All module 4 videos and notebook links can be found [here](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/04-monitoring/README.md).

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