import sys
import os
import json
import numpy as np
import pandas as pd


excel_file_path = ""
taskList = []


def help():
    help_str = '''
    ------ task distributor v02 ----------------------
    Description: This script assigns the tasks to the available slots in the most uniform distribution feasible.
    parameter:  Cyclic_Slide
                PLaPF (Pop Last and Push First)
    input: xlsx file
    output: csv file

    useage:
        To generate output with enum applied
        >    python task-distributor-v02.py input=task_data.xlsx enum=true

        To generate output without enum applied
        >    python task-distributor-v02.py input=task_data.xlsx enum=false
    -------------------------------------------------
    '''
    print(help_str)


def sum_all(data):
    sum_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for t in data.keys():
        for m in range(12):
            sum_month[m] += data[t][m]
    return sum_month


def get_avg(data):
    T = sum_all(data)
    return np.std(T, ddof=1), np.average(T)


def pop_push(data, j=-1):
    popped = data.pop(j)
    data.insert(0, popped)


def sort_all(data):
    for t in data.keys():
        data[t].sort(reverse=True)

def enum_key(target, enum ):
    keys = []
    for key, value in enum.items():
        if value == target:
            return key


def PLaPF(task_data):
    epoch_rank = []

    # get keys
    for t in task_data.keys():
        taskList.append(t)

    # sort
    sort_all(task_data)
    print('sorting...')
    print(f'\tstd,avg: {get_avg(task_data)} \n\t_sum_ : {sum_all(task_data)}')

    # Evaluate
    print('Evaluating...')
    epochs = len(taskList)*10
    print(f'\trows: {len(taskList)}')
    print(f'\tepochs: {epochs}')
    sort_all(task_data)
    for e in range(epochs):
        for t in range(len(taskList)):
            for j in range(t):
                pop_push(task_data[taskList[t]])

        std, avg = get_avg(task_data)
        epoch_rank.append(std)

    # rank for best
    best_epoch = np.argmin(epoch_rank)

    print(
        f'\tbest found at epoch at {best_epoch} epoch with std:{epoch_rank[best_epoch]}')

    # show best
    print('--- best combination ---')
    sort_all(task_data)
    for e in range(5):
        for t in range(len(taskList)):
            for j in range(t):
                pop_push(task_data[taskList[t]])

    print(f'std,avg: {get_avg(task_data)} \n _sum_ : {sum_all(task_data)}')


def Cyclic_Slide(task_data):
    epoch_rank = []

    # get keys
    for t in task_data.keys():
        taskList.append(t)

    # Evaluate
    print('Evaluating...')
    epochs = len(taskList)*10
    print(f'\trows: {len(taskList)}')
    print(f'\tepochs: {epochs}')
    for e in range(epochs):
        for t in range(len(taskList)):
            for j in range(t):
                pop_push(task_data[taskList[t]])

        std, avg = get_avg(task_data)
        epoch_rank.append(std)

    # rank for best
    best_epoch = np.argmin(epoch_rank)

    print(
        f'\tbest found at epoch at {best_epoch} epoch with std:{epoch_rank[best_epoch]}')

    # show best
    print('--- best combination ---')
    for e in range(5):
        for t in range(len(taskList)):
            for j in range(t):
                pop_push(task_data[taskList[t]])

    print(f'std,avg: {get_avg(task_data)} \n _sum_ : {sum_all(task_data)}')

def get_parameters(argv):
    parameters = {}
    for i in range(1, len(argv)):
        if '=' in argv[i]:
            name, value = argv[i].split('=')
            parameters[name] = value
    return parameters

def main():
    # Check if an input file has been provided as an argument
    PARAM=get_parameters(sys.argv)

    input_file=PARAM['input']
    if not os.path.isfile(input_file):
        print(f"the file is not valid")
        exit()
    
    parm_apply_enum=True if (PARAM['enum'].upper() in ['TRUE', 'YES']) else False
    print ('parm_apply_enum:',parm_apply_enum)
    

    # Read the JSON file and print its contents
    with open('config.json', 'r') as f:
        param = json.load(f)
        print(f"parameter: {param['parameter']}")
        print(f"output_file: {param['output_file']}")
        print("\n")
    # step 1: read the input file
    excel_file_path = input_file
    print(f'Loading from {excel_file_path}...')
    df = pd.read_excel(excel_file_path)
    task_data = df.set_index("tasks").T.to_dict("list")
    print(f'\tstd/avg: {get_avg(task_data)} \n\t_sum_ : {sum_all(task_data)}')

    # step 2: apply distribution
    print("___Process initiated!___")
    if (param['parameter'] == 'PLaPF'):
        PLaPF(task_data)
    elif (param['parameter'] =='Cyclic_Slide'):
        Cyclic_Slide(task_data)

    # step 3: Dump the best one

    filename_output = param['output_file']
    print('Saving output to csv...')

    def csv_row(tt, apply_enum=False):
        string_row = ""
        for tx in task_data[tt]:
            if apply_enum:
                string_row += enum_key(tx,param['enum'])+','
            else:
                string_row += str(tx)+','
            
        return string_row.rstrip(string_row[-1])+'\n'


    with open(filename_output, 'w') as f:
        row = 'task, JAN, FEF, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC\n'
        f.write(row)
        print(f'\t{row}')
        for t in taskList:
            row = t+','+csv_row(t, parm_apply_enum)
            f.write(row)
            print('\t', row.rstrip(row[-1]))

    f.close()


if __name__ == '__main__':
    help()
    main()
    #mask_with_enum
