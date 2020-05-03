# General

Influx is a time series database sporting a SQL style interface and query language.

Instead of tables we use measurements.
Every measurement contains tag sets (mandatory, indexed) the tuple of which forms a series. I.e, INSERT info,host=bob,location=eu and INSERT info,host=bob,location=uk forms two series (bob,eu) (bob,uk).
Every measurement also contains field sets, the (potentially NULL / empty) data for that measurement.
All fields *have* to have time.

## Examples

Select a database

USE node_health; 

Insert a measurement with one field

INSERT machine_state,host=b1,location=uk cpu_use=7.5;

Select a specific host from a measurement

SELECT * FROM machine_state WHERE host = 'b1';

Select mean CPU usage for a given host

SELECT mean("cpu_use") FROM machine_state WHERE host='b1';

Only the last 5 minutes

SELECT mean("cpu_use") FROM machine_state WHERE host='b1' GROUP BY time(5m) LIMIT 1;

# Retention Policy

Retention policies help data stop piling up.
Data is clustered into shards (Logical blocks of data clustered based on time).
Data retention policies apply to shards, not inserts.
Once a shard falls outside of its retention policy, all data in it goes bye bye.


# Python Documentation

https://influxdb-python.readthedocs.io/en/latest/api-documentation.html?highlight=create_retention_policy#influxdb.InfluxDBClient.drop_retention_policy
