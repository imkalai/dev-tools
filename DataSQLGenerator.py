# Re-run everything after code execution environment was reset

import csv
from datetime import datetime, timedelta
import random
import uuid
import pandas as pd

# Re-create the CSV file
start_time = datetime(2025, 1, 1, 0, 0, 0)
rows = []
for i in range(100):
    time = start_time + timedelta(minutes=i)
    anomaly = (i % 20 == 0)
    metric_value = round(random.uniform(90, 120), 2) if anomaly else round(random.normalvariate(50, 5), 2)
    
    row = [
        i,
        str(uuid.uuid4()),
        metric_value,
        bool(anomaly),
        time.strftime('%Y-%m-%d %H:%M:%S'),
        time.date().isoformat(),
        time.time().strftime('%H:%M:%S'),
        '1.23',
        '{"value": ' + str(metric_value) + '}',
        [1, 2, 3],
        {"anomaly": anomaly},
        None if not anomaly else 'sensitive info'
    ]
    rows.append(row)

header = [
    'id', 'uuid', 'metric_value', 'is_anomaly', 'event_time', 'event_date',
    'event_time_only', 'number_string', 'json_variant', 'json_array',
    'json_object', 'nullable_field'
]

csv_path = "/mnt/data/anomaly_data_full_types.csv"
with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)

# Convert to SQL INSERT statements
df = pd.read_csv(csv_path)

def sql_value(val):
    if pd.isna(val):
        return 'NULL'
    elif isinstance(val, str):
        val = val.replace("'", "''")
        return f"'{val}'"
    elif isinstance(val, (list, dict)):
        import json
        return f"PARSE_JSON('{json.dumps(val)}')"
    else:
        return str(val)

table_name = "anomaly_data_full_types"
sql_statements = []
for _, row in df.iterrows():
    values = ", ".join([sql_value(val) for val in row])
    sql = f"INSERT INTO {table_name} VALUES ({values});"
    sql_statements.append(sql)

sql_script = "\n".join(sql_statements)
sql_file_path = "/mnt/data/insert_anomaly_data_full_types.sql"
with open(sql_file_path, "w") as f:
    f.write(sql_script)

sql_file_path
