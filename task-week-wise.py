
from datetime import date, timedelta
import csv


def generate_weeks(year=2023, week_ends='SAT'):
    weeks = {}
    start_date = date(year, 1, 1)
    week_no = 1
    month_week_index = 1

    if week_ends == 'SAT':
        week_end_day = 5
    elif week_ends == 'SUN':
        week_end_day = 6
    else:
        return "Invalid week_ends parameter. Use 'SAT' or 'SUN'."

    current_date = start_date
    while current_date.year == year:
        week_dates = []
        month = current_date.month

        while (current_date.weekday() != week_end_day) and (current_date.year == year):
            week_dates.append(current_date)
            current_date += timedelta(days=1)

        # Add the last day of the week
        if current_date.year == year:
            week_dates.append(current_date)
            current_date += timedelta(days=1)

        weeks[week_no] = [week_dates, (month, month_week_index)]
        week_no += 1
        month_week_index += 1

        # Reset the month_week_index when the month changes
        if current_date.month != month:
            month_week_index = 1

    return weeks


def create_csv_file(filename, weeks):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['week_no', 'start_date',
                      'end_date', 'month', 'position_in_month']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for week_no, details in weeks.items():
            week_dates, month_week_index = details
            start_date = week_dates[0]
            end_date = week_dates[-1]
            month, position_in_month = month_week_index

            writer.writerow({
                'week_no': week_no,
                'start_date': start_date,
                'end_date': end_date,
                'month': month,
                'position_in_month': position_in_month
            })


def help():
    help_str = '''
    ------ task week wise ----------------------
    Description: Distributes week wise
    parameter:  
        input: xlsx file
        year: 2023

    useage:
        >    python task-week-wise.py input=task_data.xlsx year=2023

    -------------------------------------------------
    '''


def main():
    weeks = generate_weeks()
    create_csv_file('weeks.csv', weeks)


if __name__ == '__main__':
    main()
