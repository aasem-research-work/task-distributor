import sys
import os
import json
import numpy as np
import pandas as pd


excel_file_path = ""
taskList = []


def help():
    help_str = '''
    ------ task distributor v01 ----------------------
    Description: This script assigns the tasks to the available slots in the most uniform distribution feasible.
    parameter: PLaPF (Pop Last and Push First)
    input: xlsx file
    output: csv file
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


def main():
    # Check if an input file has been provided as an argument
    if len(sys.argv) < 2:
        print("Please include an input file as an argument.")
        exit()

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"the file is not valid")
        exit()

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

    # step 3: Dump the best one

    filename_output = param['output_file']
    print('Saving output to csv...')

    def csv_row(tt):
        string_row = ""
        for tx in task_data[tt]:
            string_row += str(tx)+','
        return string_row.rstrip(string_row[-1])+'\n'

    with open(filename_output, 'w') as f:
        row = 'task, JAN, FEF, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC\n'
        f.write(row)
        print(f'\t{row}')
        for t in taskList:
            row = t+','+csv_row(t)
            f.write(row)
            print('\t', row.rstrip(row[-1]))

    f.close()


if __name__ == '__main__':
    help()
    main()
