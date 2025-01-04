from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def homeScreen(request):
    return HttpResponse("Home Screen")



# tasks run sequentially, wasting time waiting for I/O operations


import time

def fetch_data(task_id):
    print(f"Fetching data for task {task_id}...")
    time.sleep(2)   
    print(f"Task {task_id} completed.")

# Sequential execution
start = time.time()
for i in range(5):
    fetch_data(i)
print(f"Total time taken: {time.time() - start:.2f} seconds")


#Solving the Problem with asyncio
#We can use asyncio for concurrent execution of I/O-bound tasks.


import asyncio

async def fetch_data(task_id):
    print(f"Fetching data for task {task_id}...")
    await asyncio.sleep(2)  # Non-blocking delay
    print(f"Task {task_id} completed.")

async def main():
    tasks = [fetch_data(i) for i in range(5)]
    await asyncio.gather(*tasks)

# Concurrent execution
start = time.time()
asyncio.run(main())
print(f"Total time taken: {time.time() - start:.2f} seconds")





