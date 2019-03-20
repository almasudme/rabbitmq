##################################################
import sys
import platform
import os

if platform.system() is 'Windows':
    root="\\\\"
else:
    root="//"

tqpath = "path_to_the Queue Manager(QM) module"
if tqpath not in sys.path:
    sys.path.insert(0,tqpath) 
##########################################################
import argparse
import glob
import QM
import tq_run
import re
import datetime
import logging
import threading
from celery.app.control import Control
from celery.result import AsyncResult
from celery.states import state, PENDING, SUCCESS, FAILURE
from celery.task.control import inspect, revoke
from itertools import chain, count
from subprocess import STDOUT, PIPE, Popen,check_output
from time import time,sleep
import socket
import kombu




def get_actualtime(timestamp):
  ts = datetime.datetime.fromtimestamp(timestamp) + datetime.timedelta(17557, 56125, 575983)
  return ts.strftime('%Y-%m-%d %H:%M:%S')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-b",         help="Used to specify the Build ID")
  parser.add_argument("-only",        help="only for this build.",
                                      action="store_true")
  args = parser.parse_args()
  build_id = args.b
  control = Control(QM.app)
  active_tasks = control.inspect().active()


  print("build id\tworker\tTaskName\tTaskID\tQueName\tStarted")
  print("active/running task:")
  print("====================")
  for  worker in active_tasks:
    tasks = active_tasks[worker]
    if len(tasks) > 0:
      print(f"\nWorker: {worker}") 
      for task in tasks:
        #    
        if build_id in task['args']:
          since = get_actualtime(task['time_start'])
          # print(since)
          print(f"[{build_id}]: {worker} : {task['name']} :{task['id']}: {task['delivery_info']['routing_key']} since:{since} {task['time_start']}")
          print("Args",end=":")
          print(task['args'])
          print("kwrgs",end=":")
          print(task['kwargs'])
        elif not args.only:
          ts = int(task['time_start']-(kombu.five.monotonic() - 9636801))
          since =   datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
          # print(since)
          print(f"[other]: {worker} : {task['name']} :{task['id']}: {task['delivery_info']['routing_key']} since: {since}")
    # else:
    #   print("None")

  reg = False
  if reg:
    registered_tasks = control.inspect().registered_tasks()
    print("registered/enabled task:")
    print("=========================")
    for  worker in registered_tasks:
      print(f"\nWorker: {worker}")  
      tasks = registered_tasks[worker]
      if len(tasks) > 0:
        for task in tasks:
          print(task)


  sch = True
  if sch:
    scheduled_tasks = control.inspect().scheduled()

    print("\nScheduled task:")
    print("==================")
    for  worker in scheduled_tasks:
      tasks = scheduled_tasks[worker]
      if len(tasks) > 0:
        for task in tasks:
          if build_id in task['args']:
            print(f"[{build_id}]: {worker} : {task['name']} :{task['id']}: {task['delivery_info']['routing_key']}")
          else:
            print(f"[other]: {worker} : {task['name']} :{task['id']}: {task['delivery_info']['routing_key']}") 
      # else:
      #   print("None")     

  qued = True
  if qued:
    reserved_tasks = control.inspect().reserved()
    print("\nreserved/queued task:")
    print("=======================")
    # print(reserved_tasks)
    for  worker in reserved_tasks:
      tasks = reserved_tasks[worker]
      if len(tasks) > 0:
        print(f"\nWorker: {worker}")  
        for task in tasks:
          if build_id in task['args']:
            print(f"[{build_id}]: {worker} : {task['name']} {task['id']} : {task['delivery_info']['routing_key']}")
            print("Args",end=":")
            print(task['args'])
            print("kwrgs",end=":")
            print(task['kwargs'])
          else:
            print(f"[other]: {worker} : {task['name']} :{task['id']}: {task['delivery_info']['routing_key']}")
            print("Args",end=":")
            print(task['args'])
            print("kwrgs",end=":")
            print(task['kwargs'])




if __name__ == "__main__":
  main()
