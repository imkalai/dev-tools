import csv
from datetime import datetime, timedelta
import random
import uuid

# Define start time
start_time = datetime(2025, 1, 1, 0, 0, 0)

# Generate rows with all Snowflake-supported data types
rows = []
for i in range(100):
    time = start_time + timedelta(minutes=i)
    anomaly = (i % 20 == 0)
    metric_value = round(random.uniform(90, 120), 2) if anomaly else round(random.normalvariate(50, 5), 2)
    
    row = [
        i,  # INTEGER
        str(uuid.uuid4()),  # STRING / TEXT
        metric_value,  # FLOAT
        bool(anomaly),  # BOOLEAN
        time.strftime('%Y-%m-%d %H:%M:%S'),  # TIMESTAMP_NTZ
        time.date().isoformat(),  # DATE
        time.time().strftime('%H:%M:%S'),  # TIME
        '1.23',  # NUMBER as STRING (for VARIANT/PARSE_JSON)
        '{"value": ' + str(metric_value) + '}',  # VARIANT
        [1, 2, 3],  # ARRAY
        {"anomaly": anomaly},  # OBJECT
        None if not anomaly else 'sensitive info'  # NULLABLE field
    ]
    rows.append(row)

# CSV header with data type hints for readability
header = [
    'id', 'uuid', 'metric_value', 'is_anomaly', 'event_time', 'event_date',
    'event_time_only', 'number_string', 'json_variant', 'json_array',
    'json_object', 'nullable_field'
]

# Save to CSV
csv_path = "/mnt/data/anomaly_data_full_types.csv"
with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)

csv_path
