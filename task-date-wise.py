import os
import sys
import warnings
import json
from openpyxl import load_workbook
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import timedelta, date

warnings.simplefilter(action='ignore', category=FutureWarning)

taskList = []

def get_parameters(argv):
    parameters = {}
    for i in range(1, len(argv)):
        if '=' in argv[i]:
            name, value = argv[i].split('=')
            parameters[name] = value
    return parameters


def read_excel_sheet(path_excel_file, sheet_name):
    df = pd.read_excel(path_excel_file, sheet_name=sheet_name)
    return df

def greedy_scheduler_cal(ASSETNUM_list, d, start_date):
    frequency="M"
    n=len(ASSETNUM_list)
    ### Greedy schedule #######
    schedule = [0] * d  # initialize empty schedule with d days
    calender_days=[]
    for i in range(n):
        min_day = schedule.index(min(schedule))  # find the day with the least jobs scheduled so far
        schedule[min_day] += 1  # add the job to the day with the least jobs scheduled so far

    ### CSV as per schedule #######
    asset_index=-1
    with open("task_date_wise.csv","w") as f:
        f.write('ASSETNUM,INDEX,FREQUENCY,DATED\n')
        for j in range(len(schedule)):
            for k in range(schedule[j]):
                cal_day=start_date+timedelta(days=j)                
                asset_index+=1
                row= f'{ASSETNUM_list[asset_index]},{k},{frequency},{str(cal_day)}\n'
                #row= f'{asset_index},{k},{frequency},{str(cal_day)}\n'
                f.write(row)
    return schedule, calender_days

def help():
    help_str = '''
    ------ task-date-wise.py ----------------------
    Description: This script distributes the assets in dates
    parameter: 
        input: xlsx file
        month: JAN, FEF, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC

    useage:
        >    python input=<path_to_excelfile> month=<any_month>
    example:
        >    python task-date-wise.py input="task_data.xlsx" month="JAN"
    -------------------------------------------------
    '''
    print(help_str)

if __name__ == '__main__':
    PARAM = get_parameters(sys.argv)

    if ( 'input' not in PARAM) or ('month' not in PARAM):
        help()
        exit()

    if 'frequency' in PARAM:
        input_frequency=PARAM['frequency']
    else:
        input_frequency=1
    
    d=30 # number of days {frequency:1[M]->30};{frequency:3[Q]->90};{frequency:6[SA]->180};{frequency:12[A]->365}


    input_month = PARAM['month']
    month_list=['JAN', 'FEF', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    if input_month not in month_list:
        print(f"No or Invalid month found!")
        print (f"valid months are: {month_list}")
        exit()
    input_file = PARAM['input']
    #input_file = "task_data.xlsx"
    if not os.path.isfile(input_file):
        print(f"the file is not valid")
        exit()

    df_DATA=read_excel_sheet(input_file,"DATA")
    df_DATA=df_DATA['ASSETNUM'].loc[df_DATA[input_month] == input_frequency]
    ASSETNUM_list=df_DATA.to_list()

    
    sd = date(2023, 4, 1) #starting date

    schedule,cal_days = greedy_scheduler_cal(ASSETNUM_list, d, sd)


