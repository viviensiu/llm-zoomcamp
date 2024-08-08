## Module 5: LLM Orchestration
**Credits**
- Shout out to [Tommy Dang](https://github.com/tommydangerous) of [MageAI](https://github.com/mage-ai) for creating and providing the lessons of this module. All files and folders under ```rag-project``` are cloned from [this repo](https://github.com/mage-ai/rag-project).
- All module 5 videos and notebook links can be found [here](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/05-orchestration/README.md).

### Pre-requisites
- Clone the Module 5 repo to local folder.
```bash
git clone https://github.com/mage-ai/rag-project
```
- **If you would like to add the cloned repo into your own LLM zoomcamp repo and manage everything under one Git repo**, execute the following in ```rag-project``` folder to remove its git configuration and history:
```bash
git remote remove origin
rm -rf .git
```
- Then create a new folder ```module 5``` in your local LLM zoomcamp repo, and copy-paste ```rag-project``` folder into ```module 5``` folder.   
- Run 
```bash
cd rag-project
./scripts/start.sh
```
- Verify that ```start.sh``` completed successfully by checking Mage at [http://localhost:6789/](http://localhost:6789/)
- For more setup information, refer to these [instructions](https://docs.mage.ai/getting-started/setup#docker-compose-template).

### 5.0 Module overview
- How to use Mage to manage RAG orchestration, particularly in data preparation: ingest > transform > storing.
- To create a pipeline in Mage, 
    1. Go to ```+ New Pipeline --> Retrieval Augmented Generation```.
    2. There are 2 main pipelines for this: Data Preparation and Inference (handles user prompts).
    3. Data Preparation: 4 stages, load (ingesting data), transform (chunking, tokenising, embedding data), export (save to vector db), index (optimise by indexing data in vector db for efficient search)
- To view all created pipelines, click on ```Pipelines``` on main page. To open a pipeline, right click and select ```Open Pipeline```.

### 5.1 Ingest
Steps:
1. From ```+ New Pipeline --> Retrieval Augmented Generation```, click on ```Load --> Go --> Ingest --> Go```.
2. Under ```Ingest```, click on ```Add block```: As we have ingested data from Github in previous modules, we will select ```API Data loader``` to fetch the data. 
3. ```API Data loader```: Copy-paste this [url](https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/01-intro/documents.json) under ```Endpoint URL```, then click ```Run```.
4. We can then see the output by clicking on ```Load output results```.
5. To look at the code running under ```API Data loader```, go back to ```API Data loader``` and click on ```Edit``` which also allows you to customise the code.

### 5.2 Chunk
Steps:
1. (Continuing from 5.1 where our data is loaded into the API Data Loader). Go to the top bar where you can see ```Data Preparation | Load | Ingest``` and click on ```Load --> Transform --> Chunking```
2. Click on ```Chunking --> Add Block --> Custom Code```. There are many existing chunking methods provided by Mage but as our data source is sort-of chunked already by "Question", "Course", "Answer", hence we will use our [custom code](https://github.com/mage-ai/rag-project/blob/master/llm/rager/transformers/radiant_photon.py) to perform chunking.
3. Copy-paste to replace the [custom code](https://github.com/mage-ai/rag-project/blob/master/llm/rager/transformers/radiant_photon.py) inside this block, and click on the purple run button. Once it finishes execution, you should see something that shows ```Documents: 948```.
4. If you look at the output from Step 3, It shows that the custom code is combining the course, section, question and answer into a single chunk (separated by line break) for each document, and each chunk has a document id that will be used for retrieval at a later stage.

### 5.3 Tokenization
1. (Continuing from 5.2 where our data is chunked). Go to top bar ```Data Preparation | Transform | Chunking``` and click on ```Transform --> Tokenization```.
2. Click on ```Tokenization --> Add Block```. There are multiple tokenization strategies made available here, for our use case we will choose ```Lemmatization(spaCY)```.
3. We will replace the existing code with our [custom code](https://github.com/mage-ai/rag-project/blob/master/llm/rager/transformers/vivid_nexus.py) as we would like to include progress printing during tokenization. Click on ```Edit``` and copy-paste the [custom code](https://github.com/mage-ai/rag-project/blob/master/llm/rager/transformers/vivid_nexus.py) inside. Click on the purple run button.
4. Once tokenization is completed, we can see there's a new column "tokens" containing a list of tokens generated from the text chunk.

### 5.4 Embedding
1. (Continuing from 5.3 where our data is tokenized). Go to top bar ```Data Preparation | Transform | Tokenization``` and click on ```Transform --> Embed```.
2. Under ```Add Block```, there are a multitude of embedding methods for selection (depends on your use case).
3. We will be using ```spaCy Embeddings```. Copy-paste the [code chunk](https://github.com/mage-ai/rag-project/blob/master/llm/rager/transformers/prismatic_axiom.py) inside the block and execute as usual.
4. Once it's done, we can see that there's a new field ```embedding``` created, which contains the vector of embeddings and its dimensions depend on the choice of embedding method used.

### 5.5 Export
1. This is the final stage in data preparation as we will export our chunked and embedded data into a vector database.
2. (Continuing from 5.4 where our data is tokenized). Go to top bar ```Data Preparation | Transform | Embed``` and click on ```Transform --> Export --> Vector Database```.
3. As we have used ```ElasticSearch``` in previous modules, we will use this as the Vector DB.
4. As we are running ES from a Docker container, we will update the ```Connection string``` to use the service name of the elasticsearch service inside docker compose file, followed by the port as the connection string, e.g ```<docker-compose-service-name><port>```. For our case, it's [http://elasticsearch:9200](http://elasticsearch:9200).
5. We also copy-paste the codes from this [source](https://github.com/mage-ai/rag-project/blob/master/llm/rager/data_exporters/numinous_fission.py) into the code block. Now we are ready to export our processed data.
6. After running it we shouldn't expect any output since this is indexing our processed data into an ES Index.
