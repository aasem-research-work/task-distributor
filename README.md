# Task Distributor
Description: This script assigns the tasks to the available slots in the most uniform distribution feasible.  


# Usage
## Environmnet:  
Assuming conda ( [miniconda](https://docs.conda.io/en/latest/miniconda.html) ) is installed.   
> conda create -n sch python=3.10  
> conda activate sch   
> pip install -r requirements.txt 

## Run     
Prepare data:   
    `python task-distributor-v05.py input=task_data.xlsx`  

date wise distribution  
    `python task-date-wise.py input="task_data.xlsx" month="JAN"`  
    
week wise distribution  
    `python task-week-wise.py year=2023` 
