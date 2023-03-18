# Task Distributor V01
    Description: This script assigns the tasks to the available slots in the most uniform distribution feasible.  
    parameter: PLaPF (Pop Last and Push First). 
    input: xlsx file. 
    output: csv file. 

# Usage
Environmnet:  
> conda create -n sch python=3.10  
> conda activate sch   
> pip install -r requirements.txt 

Run
> python task_distributor_v1.py task_data.xlsx  
