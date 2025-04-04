from flask import Blueprint, request, jsonify
from src.agents.interview_scheduler.scheduler import InterviewScheduler

scheduling_bp = Blueprint('scheduling', __name__)
interview_scheduler = InterviewScheduler()

@scheduling_bp.route('/schedule', methods=['POST'])
def schedule_interview():
    data = request.json
    candidate_email = data.get('candidate_email')
    interview_time = data.get('interview_time')
    job_position = data.get('job_position')

    if not candidate_email or not interview_time or not job_position:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        interview_scheduler.schedule_interview(candidate_email, interview_time, job_position)
        interview_scheduler.send_invitation(candidate_email, interview_time, job_position)
        return jsonify({'message': 'Interview scheduled successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500