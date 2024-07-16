## Open source data ingestion for RAGs with dlt by Akela Drissner
<b>Goal</b>: Allows ingestion of data from multiple sources into a schematic data pipeline using dlt.
<b>Tools</b>: dlt, LanceDB, Ollama.

### References:
- [Workshop slides](https://github.com/viviensiu/llm-zoomcamp/blob/main/dlt%20workshop/dlt.LLM.Zoomcamp.pdf)
- [Workshop recording](https://www.youtube.com/live/qUNyfR_X2Mo?si=6h89NMTYgmgBfxn4)
- [Workshop notebook](https://colab.research.google.com/drive/1nNOybHdWQiwUUuJFZu__xvJxL_ADU3xl?usp=sharing)

### What is dlt (data load tool)?
- Python library that automates data loading with features e.g. schema creation, normalization and integration adaptability.
- [Official Page of dlthub](https://dlthub.com/docs/intro)

### How dlt works?
- You'll need a resource, a pipeline and a destination (example: LanceDB):
    - Define a ```dlt.resource``` decorator function to load data from data sources like JSON, Requests, Notion, etc.
    - Define a ```dlt.pipeline``` for ingestion. Specify its destination (e.g. LanceDB) and dataset name.
    - Pass the resource and its table name into pipeline.run(), so the resource will get ingested by dlt into the destination dataset with the defined table name.
    - There is also an option to embed the data inside the pipeline by using adapters e.g. ```lancedb_adapter```. The embedding model env. variables need to be setup beforehand. 
    - Once the resource is ingested, you can find the dataset and table by connecting to LanceDB and view the tables contained in this dataset.
- the ```dlt.resource``` decorator could also be modified to allow incremental loading, which speeds up ingestion as only data with changes would be replaced inside the destination table, instead of reingesting the whole dataset again.

### dlt for RAG
- Once the data is ingested into the vector DB, it can be used for query-based context retrieval. 
- Context is then passed to LLM for response generation.

### Homework
- Link to [homework questions](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2024/workshops/dlt.md)
