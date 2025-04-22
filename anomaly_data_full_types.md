CREATE OR REPLACE TABLE anomaly_data_full_types (
    id INTEGER,
    uuid STRING,
    metric_value FLOAT,
    is_anomaly BOOLEAN,
    event_time TIMESTAMP_NTZ,
    event_date DATE,
    event_time_only TIME,
    number_string STRING,
    json_variant VARIANT,
    json_array ARRAY,
    json_object OBJECT,
    nullable_field STRING
);
