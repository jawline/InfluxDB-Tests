import sys
import socket
import psutil
import time

from influxdb import InfluxDBClient

db_name="funtime"

client = InfluxDBClient(host='localhost', port=int(sys.argv[-1]), username='root', password='root', database=db_name)

print("Create database: " + db_name)
client.create_database(db_name)

print("Create a retention policy")
client.drop_retention_policy('awesome_policy')
client.create_retention_policy('awesome_policy', '3d', 100, default=True)

def log_status():
  json_body = [
      {
          "measurement": "server_state",
          "tags": {
              "host": socket.gethostname() + sys.argv[-2]
          },
          "fields": {
              "cpu_state": psutil.cpu_percent(),
              "memory_use": psutil.virtual_memory()[1],
              "memory_max": psutil.virtual_memory()[0],
              "memory_percent": psutil.virtual_memory()[2]
          }
      }
  ]
  client.write_points(json_body)

while True:
  print("Logging status")
  log_status()
  time.sleep(5)
