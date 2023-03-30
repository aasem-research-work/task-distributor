# Task Distributor
Description: This script assigns the tasks to the available slots in the most uniform distribution feasible.  
parameter:  Cyclic_Slide   
            PLaPF (Pop Last and Push First)   
input/output: xlsx file  

# Usage
## Environmnet:  
Assuming conda ( [miniconda](https://docs.conda.io/en/latest/miniconda.html) ) is installed.   
> conda create -n sch python=3.10  
> conda activate sch   
> pip install -r requirements.txt 

## Run     
    python task-distributor-v05.py input=task_data.xlsx 

