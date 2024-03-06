import csv
from datetime import datetime, timedelta

def calculate_dates(records):
    for i in range(len(records) - 1):
        try:
            records[i]['End Date'] = datetime.strptime(records[i + 1]['Effective Date'], '%d-%m-%Y') - timedelta(days=1)
        except ValueError:
            records[i]['End Date'] = records[i]['Effective Date']
    records[-1]['End Date'] = datetime(2100, 1, 1)  # Far-future date for the last record
    return records

def transform_data(input_file, output_file):
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    data = calculate_dates(data)

    transformed_data = []

    for record in data:
        employee_code = record['Employee Code']
        manager_employee_code = record['Manager Employee Code']
        last_compensation = record.get('Last Compensation', 0)  # Default value for 'Last Compensation'
        variable_pay = record.get('Variable Pay', 0)  # Default value for 'Variable Pay'
        tenure_in_org = record.get('Tenure in Org', 0)  # Default value for 'Tenure in Org'

        end_date = datetime.strptime(str(record['End Date']), '%Y-%m-%d %H:%M:%S')  # Convert to datetime

        current_date = datetime.strptime(record['Effective Date'], '%d-%m-%Y')

        while current_date <= end_date:
            transformed_record = {
                'Employee Code': employee_code,
                'Manager Employee Code': manager_employee_code,
                'Last Compensation': last_compensation,
                'Variable Pay': variable_pay,
                'Tenure in Org': tenure_in_org,
                'Effective Date': current_date.strftime('%d-%m-%Y'),
                'End Date': (current_date + timedelta(days=1)).strftime('%d-%m-%Y')
            }
            transformed_data.append(transformed_record)

            current_date += timedelta(days=1)

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=transformed_data[0].keys())
        writer.writeheader()
        writer.writerows(transformed_data)

input_file_path = 'input.csv'
output_file_path = 'output.csv'

transform_data(input_file_path, output_file_path)


