import sys
import socket
import psutil
import time

from influxdb import InfluxDBClient

db_name="funtime"

client = InfluxDBClient(host='localhost', port=int(sys.argv[-1]), username='root', password='root', database=db_name)

#SCAN_PERIOD="5m"
#CPU_QUERY = 'SELECT mean("cpu_state") INTO "cpu_mean" FROM "server_state" GROUP BY time({0})'.format(SCAN_PERIOD);
#RAM_QUERY = 'SELECT mean("memory_percent") INTO "ram_mean" FROM "server_state" GROUP BY time({0})'.format(SCAN_PERIOD);
#client.drop_continuous_query('cpu_mean'); 
#client.drop_continuous_query('ram_mean'); 
#client.create_continuous_query('cpu_mean', CPU_QUERY, db_name, 'EVERY {0}'.format(SCAN_PERIOD)); 
#client.create_continuous_query('ram_mean', RAM_QUERY, db_name, 'EVERY {0}'.format(SCAN_PERIOD)); 

def print_host(host):
  
  recent_logs = client.query('SELECT * FROM server_state WHERE host=\'{0}\' LIMIT 1'.format(host))
  

  if sum(1 for _ in recent_logs.get_points()) == 0:
    print("Not Logging - Down")

  for log_line in recent_logs.get_points():
    for item in log_line.keys():
      print(item + ':', log_line[item])
  #print("{0}".format(client.query('SELECT * FROM cpu_mean LIMIT 1')))
  #print("{0}".format(client.query('SELECT * FROM ram_mean LIMIT 1')))
  for avg_free_mem in client.query('SELECT (sum("memory_use") / sum("memory_max")) * 100 FROM server_state WHERE host=\'{0}\' GROUP BY time(5m) LIMIT 1'.format(host)).get_points():
    print('Average Free Memory (Last 5m):', avg_free_mem['sum_sum'])
  #print(client.get_list_continuous_queries())

while True:
  hosts = client.query('SHOW TAG VALUES FROM "server_state" WITH KEY = "host"')
  for host in hosts.get_points():
    print(host['value'])
    print_host(host['value'])
  time.sleep(15)
