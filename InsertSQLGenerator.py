# Load the CSV file and convert each row into an SQL INSERT statement
insert_statements = []
table_name = "anomaly_data_full_types"

with open(csv_path, newline='') as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip header
    for row in reader:
        # Properly quote and format values
        values = []
        for val in row:
            if val == '':
                values.append('NULL')
            elif val.lower() in ['true', 'false']:
                values.append(val.upper())
            elif val.startswith('{') or val.startswith('['):  # JSON types
                values.append(f"PARSE_JSON('{val}')")
            elif val.isdigit() or val.replace('.', '', 1).isdigit():
                values.append(val)
            else:
                values.append(f"'{val}'")
        insert_stmt = f"INSERT INTO {table_name} ({', '.join(header)}) VALUES ({', '.join(values)});"
        insert_statements.append(insert_stmt)

# Combine into a single SQL script
sql_script = "\n".join(insert_statements)
sql_script[:2000]  # Preview the first 2000 characters of the SQL script
