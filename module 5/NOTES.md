## Module 5: LLM Orchestration
**Credits**
All files and folders under ```rag-project``` are cloned from [this rep]o(https://github.com/mage-ai/rag-project)

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