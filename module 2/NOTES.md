## Module 2: Open-Source LLMs

### 2.1 Introduction
Motivation: Replacing OpenAI in Module 1 with open-source LLM

### Using SaturnCloud for GPU Notebooks
- Goal: Setup SaturnCloud account to have access to their GPU to run open-source LLM.
- [Closed on 25th June 2024] Register for an account with free GPU access at LLM Zoomcamp website.
- Log on to Saturn Cloud and setup the following:
1. Secrets: Store your API keys for various oepn-source LLMs here (e.g. HuggingFace API key)
2. User -> Manage <user name> -> "Git SSH Key": copy-paste your Github SSH Public Key here to allow access from your SaturnCloud to your Github.
3. Resources: click on "new Python Server" 
    - Overview: fill in notebook name.
    - Hardware: select "GPU", Size: select "T4 XLarge - 4 cores - 16GiRAM - 1 GPU".
    - "Environment" -> "Image": "saturncloud/saturn-python-llm".
    - "Extra packages" -> "Pip": ```pip install -U transformers accelerate bitsandbytes```
    - "Git repositores": copy-paste the SSH path of your personal Git repo created for this module. Path should look like "git@github.com..............git".
    - Finally, click "Create".
4. Under the newly-created Jupyter server, go to "Secrets and Roles" tab. Click on "Attach Secret Environment Variable" and select the API key which was previously setup in Step 1.
5. Go to "Overview" tab and click "Start".
6. Once the server is up, click on "Jupyter Notebook" to start the notebook.