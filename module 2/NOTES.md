## Module 2: Open-Source LLMs

### 2.1 Introduction
Motivation: Replacing OpenAI in Module 1 with open-source LLM

### 2.2 Using SaturnCloud for GPU Notebooks
- Goal: Setup [SaturnCloud](https://saturncloud.io/) account to have access to their GPU to run open-source LLM.
- [Closed on 25th June 2024] Register for an account with free GPU access at LLM Zoomcamp website.
- Log on to Saturn Cloud and setup the following:
1. Secrets: Store your API keys for various open-source LLMs here (e.g. HuggingFace API key)
2. User -> Manage \<user name\> -> "Git SSH Key": click on "Create SSH key", then paste this key to your Github SSH Public Key (under your Github profile -> Settings -> SSH and GPG Keys -> click on "New SSH Key" and copy-paste in "Key") to allow access from your SaturnCloud to your Github. Also see [Official guide](https://saturncloud.io/docs/using-saturn-cloud/gitrepo/?_gl=1*1tevkte*_gcl_au*OTgyMTk1MjUuMTcxOTI1ODQ5OC4xNzg2ODQyMDY1LjE3MTkzOTU0MzIuMTcxOTM5NTQ1Mg..*_ga*MTI1OTcxODE1NC4xNzE5MjU4NDk4*_ga_9QKGCS5Q41*MTcxOTQwNzAzMC41LjAuMTcxOTQwNzAzMC42MC4wLjA.#set-up-git-ssh-keys).
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

### 2.3 HuggingFace and Google FLAN T5
- Link to [Google FLAN-T5 XL](https://huggingface.co/google/flan-t5-xl)

