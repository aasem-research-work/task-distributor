# Task Distributor V01
    Description: This script assigns the tasks to the available slots in the most uniform distribution feasible.  
    parameter: PLaPF (Pop Last and Push First). 
    input: xlsx file. 
    output: csv file. 

# Usage
## Environmnet:  
Assuming conda ( [miniconda](https://docs.conda.io/en/latest/miniconda.html) ) is installed.   
> conda create -n sch python=3.10  
> conda activate sch   
> pip install -r requirements.txt 

## Run
> python task-distributor-v01.py task_data.xlsx  

