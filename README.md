# Task Distributor
Description: This script assigns the tasks to the available slots in the most uniform distribution feasible.  
parameter:  Cyclic_Slide
            PLaPF (Pop Last and Push First)
input: xlsx file. 
output: csv file. 

# Usage
## Environmnet:  
Assuming conda ( [miniconda](https://docs.conda.io/en/latest/miniconda.html) ) is installed.   
> conda create -n sch python=3.10  
> conda activate sch   
> pip install -r requirements.txt 

## Run  
To generate output with enum applied:    
    `python task-distributor-v02.py input=task_data.xlsx enum=true`

To generate output without enum applied:   
    `python task-distributor-v02.py input=task_data.xlsx enum=false`
