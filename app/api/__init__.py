from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user # type: ignore
import redis
import time
import datetime
import json
# import traceback

from ..models import db, Job
from .types import JobCreateRequest, JobResponse
from .jobs import job_types, REDIS_QUEUE
from ..env import REDIS_HOSTNAME, REDIS_HOSTPORT

api = Blueprint('api', __name__)

redis_client = redis.StrictRedis(host=REDIS_HOSTNAME, port=REDIS_HOSTPORT, db=0)

@api.route('/jobs')
@login_required
def get_jobs():
    jobs_of_user = current_user.jobs
    res: list[JobResponse] = [JobResponse(**job) for job in jobs_of_user]
    return jsonify(res)

@api.route('/jobs/<int:job_id>')
@login_required
def get_job_by_id(job_id: int):
    job = current_user.jobs.filter_by(id=job_id).first()
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return JobResponse.model_validate(job.to_dict()).model_dump()

@api.route('/jobs', methods=['POST'])
@login_required
def create_job():
    R = JobCreateRequest.model_validate(request.get_json())

    for job_type in job_types:
        if job_type.job_type == R.type:
            started_at = time.time()

            try:
                if job_type.immediate:
                    output = job_type(R.input)
                    ended_at = time.time()
                    return jsonify(
                        JobResponse.model_validate(dict(
                            id=-1, type=R.type, status="COMPLETED", started_at=started_at, ended_at=ended_at, input=R.input, output=output,
                        )).model_dump()
                    )
                else:
                    job = Job()
                    job.type = R.type
                    job.started_at = datetime.datetime.fromtimestamp(started_at)
                    job.ended_at = datetime.datetime.fromtimestamp(started_at)
                    job.status = "PENDING"
                    job.input = R.input
                    job.output = ""
                    job.users.append(current_user)

                    db.session.add(job)
                    db.session.commit()

                    job_payload = JobResponse.model_validate(job.to_dict()).model_dump()
                    redis_client.rpush(REDIS_QUEUE, json.dumps(job_payload))

                    return jsonify(job_payload)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
                # return jsonify({'error': traceback.format_exc()}), 500

    return jsonify({
        'error': "Unknown job type",
    }), 400
