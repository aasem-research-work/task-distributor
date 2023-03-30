import os
import sys
import warnings
import json
from openpyxl import load_workbook
import pandas as pd
import numpy as np
from tqdm import tqdm

warnings.simplefilter(action='ignore', category=FutureWarning)


excel_file_path = ""
taskList = []


def help():
    help_str = '''
    ------ task distributor v05 ----------------------
    Description: This script assigns the tasks to the available slots in the most uniform distribution feasible.
    parameter:  Cyclic_Slide
                PLaPF (Pop Last and Push First)
    input: xlsx file
    output: xlsx file

    useage:
        >    python task-distributor-v05.py input=task_data.xlsx

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


def enum_key(target, enum):
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


def Cyclic_Slide(task_data, epoch_multiplier):
    epoch_rank = []

    # get keys
    for t in task_data.keys():
        taskList.append(t)

    # Evaluate
    print('Evaluating...')
    epochs = len(taskList)*epoch_multiplier
    print(f'\trows: {len(taskList)}')
    print(f'\tepochs: {epochs}')

    for e in tqdm(range(epochs)):
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
    for e in tqdm(range(5)):  # Just how fist file rows for display purpose
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


def read_excel_sheet(path_excel_file, sheet_name):
    df = pd.read_excel(path_excel_file, sheet_name=sheet_name)
    return df


def write_excel_sheet(path_excel_file, sheet_name, data_Frame):
    book = load_workbook(path_excel_file)
    writer = pd.ExcelWriter(path_excel_file, engine='openpyxl')
    writer.book = book
    data_Frame.to_excel(writer, sheet_name=sheet_name,
                        index=False, header=True)
    writer.close()


def merge_dataframes(df_master, df_input, common_col='TYPE', add_type=False):
    # Merge the two dataframes on the 'TYPE' column
    merged_df = pd.merge(df_master, df_input, on=common_col)

    # Define the list of month column names
    month_cols = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                  'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    # Create a list of column names for the final dataframe
    if add_type:
        cols = ['TYPE', 'ASSETNUM'] + month_cols
    else:
        cols = ['ASSETNUM'] + month_cols

    # Create a new dataframe with the selected columns
    #print (cols)
    result_df = merged_df[cols]

    return result_df


def main():
    # Check if an input file has been provided as an argument
    PARAM = get_parameters(sys.argv)

    input_file = PARAM['input']
    #input_file = "task_data.xlsx"
    if not os.path.isfile(input_file):
        print(f"the file is not valid")
        exit()

    # Read the JSON file and print its contents
    with open('config.json', 'r') as f:
        param = json.load(f)
        epoch_multiplier = param['epoch_multiplier']
        print(f"parameter: {param['parameter']}")
        print(f"epoch_multiplier: {epoch_multiplier}")
        print("\n")
    # step 1: read the input file
    excel_file_path = input_file
    print(f'Loading from {excel_file_path}...')
    df_master = read_excel_sheet(excel_file_path, 'MASTER')
    df_input = read_excel_sheet(excel_file_path, 'INPUT')
    df_data = merge_dataframes(df_master, df_input)
    df_data_typed = merge_dataframes(df_master, df_input, add_type=True)
    write_excel_sheet(excel_file_path, 'DATA', df_data)

    task_data = df_data.set_index("ASSETNUM").T.to_dict("list")
    print(f'\tstd/avg: {get_avg(task_data)} \n\t_sum_ : {sum_all(task_data)}')

    # step 2: apply distribution
    print("___Process initiated!___")
    if (param['parameter'] == 'PLaPF'):
        PLaPF(task_data, epoch_multiplier)
    elif (param['parameter'] == 'Cyclic_Slide'):
        Cyclic_Slide(task_data, epoch_multiplier)

    # step 3: Dump the best one
    print('Saving output...')

    def csv_row(tt, apply_enum=""):
        string_row = ""
        for tx in task_data[tt]:
            if apply_enum == "enum":
                string_row += enum_key(tx, param['enum'])+','
            elif apply_enum == "cost":
                #string_row += enum_key(tx, param['cost'])+','
                string_row += get_cost(assetnum=tt,
                                       enum=tx, cost_json=param)+','
            else:
                string_row += str(tx)+','

        return string_row.rstrip(string_row[-1])+'\n'
    '''
    def get_cost(assetnum, enum, cost_json):
        assettype=df_data_typed [df_data_typed['ASSETNUM']==assetnum]['TYPE'].iloc[0]
        labor_cost=cost_json[assettype][enum]
        return labor_cost
    '''
    with open('tmp.txt', 'w') as f:
        row = 'ASSETNUM, JAN, FEF, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC\n'
        f.write(row)
        for t in taskList:
            row = t+','+csv_row(t, "")
            f.write(row)
    f.close()
    df_scheduled = pd.read_csv('tmp.txt')
    write_excel_sheet(excel_file_path, 'EVALUATE', df_scheduled)

    with open('tmp.txt', 'w') as f:
        row = 'ASSETNUM, JAN, FEF, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC\n'
        f.write(row)
        for t in taskList:
            row = t+','+csv_row(t, "enum")
            f.write(row)
    f.close()
    df_scheduled = pd.read_csv('tmp.txt')
    write_excel_sheet(excel_file_path, 'SCHEDULED', df_scheduled)

    def get_cost(assetnum, enum, cost_json):
        assettype = df_data_typed[df_data_typed['ASSETNUM']
                                  == assetnum]['TYPE'].iloc[0]
        labor_cost = cost_json['cost'][assettype][str(enum)]
        return labor_cost

    with open('tmp.txt', 'w') as f:
        row = 'ASSETNUM, JAN, FEF, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC\n'
        f.write(row)
        for t in taskList:

            row = t+','+csv_row(t, "cost")
            f.write(row)
    f.close()
    df_scheduled = pd.read_csv('tmp.txt')
    write_excel_sheet(excel_file_path, 'COST', df_scheduled)


if __name__ == '__main__':
    help()
    main()
    # mask_with_enum
