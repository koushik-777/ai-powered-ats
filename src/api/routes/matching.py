from flask import Blueprint, request, jsonify
from src.agents.matching_algorithm.matcher import Matcher

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/match', methods=['POST'])
def match_candidates():
    data = request.json
    job_description = data.get('job_description')
    candidate_cv = data.get('candidate_cv')

    if not job_description or not candidate_cv:
        return jsonify({'error': 'Job description and candidate CV are required.'}), 400

    matcher = Matcher()
    match_percentage, details = matcher.compare(job_description, candidate_cv)

    return jsonify({
        'match_percentage': match_percentage,
        'details': details
    })