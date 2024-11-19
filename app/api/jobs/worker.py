import redis
import json
from multiprocessing import Process
import app.env as ENV
import app.models as MODELS
from flask import Flask
import sys
import os
from .constants import REDIS_QUEUE

def print_threadsafe(msg: str):
    # https://stackoverflow.com/a/75368797/13680015
    os.write(sys.stdout.fileno(), f"{msg}\n".encode())

def worker_process(worker_id: int, app: Flask):
    redis_client = redis.StrictRedis(host=ENV.REDIS_HOSTNAME, port=ENV.REDIS_HOSTPORT, db=0)

    with app.app_context():  # Ensure app context for database operations
        print_threadsafe(f"Worker {worker_id} started.")

        while True:
            # Blocking pop from the queue
            _, job_data = redis_client.blpop(REDIS_QUEUE) # type: ignore
            job = json.loads(job_data) # type: ignore
            job_id = job['id']

            print_threadsafe(f"Worker {worker_id} processing job {job_id}.")

            try:
                # Simulate processing (replace this with your actual computation)
                output = process_job(job)

                # Update the job in the database
                db_job = MODELS.Job.query.get(int(job_id))
                if not db_job:
                    raise Exception(f"Job {job_id} not found in the database.")

                db_job.status = 'COMPLETED'
                db_job.output = output
                db_job.ended_at = MODELS.db.func.now()
                MODELS.db.session.commit()

                print_threadsafe(f"Worker {worker_id} completed job {job_id}.")
            except Exception as e:
                db_job = MODELS.Job.query.get(job_id)
                if not db_job:
                    print_threadsafe(f"Job {job_id} not found in the database.")
                    continue
                db_job.status = 'FAILED'
                db_job.output = str(e)
                MODELS.db.session.commit()
                print_threadsafe(f"Worker {worker_id} failed job {job_id}: {e}")

from multiprocessing import cpu_count

processes: list[Process] = []
def start_worker_pool(app: Flask):
    stop_worker_pool()
    num_workers = max(1, cpu_count() - 2)
    for i in range(num_workers):
        p = Process(target=worker_process, args=(i, app))
        p.start()
        processes.append(p)
    print_threadsafe(f"Started {num_workers} worker processes.")

def stop_worker_pool():
    if processes:
        N = len(processes)
        for p in processes:
            try:
                p.terminate()
            except Exception as e:
                print_threadsafe(f"Error stopping worker process: {e}. Still continuing.")
        processes.clear()
        print_threadsafe(f"Stopped all {N} jobs in the worker pool.")
    else:
        print_threadsafe("No processes in worker pool to stop.")

import atexit
atexit.register(stop_worker_pool)

import signal
import typing
def cleanup(*args: typing.Any):
    stop_worker_pool()
    exit(0)
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

from .job_types import job_types
from typing import Any

def process_job(job_to_process: dict[str, Any]) -> str:
    for job_type in job_types:
        if job_type.job_type == job_to_process['type']:
            return job_type(job_to_process['input'])
    raise ValueError(f"Unknown job type: {job_to_process['type']}")
