from flask import Blueprint, jsonify
from flask_login import login_required, current_user

api = Blueprint('api', __name__)

@api.route('/jobs')
@login_required
def get_jobs():
    jobs_of_user = current_user.jobs
    return jsonify([job.to_dict() for job in jobs_of_user])
