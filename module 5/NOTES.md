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
1. (Continuing from 5.1 where our data is loaded into the API Data Loader). Go to the top bar where you can see ```Data Preparation | Load | Ingest``` and click on ```Load --> Transform --> Chunking'''
2. Click on ```Chunking --> Add Block --> Custom Code```. There are many existing chunking methods provided by Mage but as our data source is sort-of chunked already by "Question", "Course", "Answer", hence we will use our [custom code](https://github.com/mage-ai/rag-project/blob/master/llm/rager/transformers/radiant_photon.py) to perform chunking.
3. Copy-paste to replace the [custom code](https://github.com/mage-ai/rag-project/blob/master/llm/rager/transformers/radiant_photon.py) inside this block, and click on the purple run button. Once it finishes execution, you should see something that shows ```Documents: 948```.
4. If you look at the output from Step 3, It shows that the custom code is combining the course, section, question and answer into a single chunk (separated by line break) for each document, and each chunk has a document id that will be used for retrieval at a later stage.
