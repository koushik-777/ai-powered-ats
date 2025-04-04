from flask import Blueprint, request, jsonify
from src.agents.shortlisting_system.shortlister import Shortlister

shortlisting_bp = Blueprint('shortlisting', __name__)
shortlister = Shortlister()

@shortlisting_bp.route('/shortlist', methods=['POST'])
def shortlist_candidates():
    data = request.json
    job_id = data.get('job_id')
    candidates = data.get('candidates')
    
    if not job_id or not candidates:
        return jsonify({'error': 'Job ID and candidates are required.'}), 400
    
    shortlist = shortlister.filter_candidates(job_id, candidates)
    return jsonify(shortlist), 200

@shortlisting_bp.route('/shortlist/ranked', methods=['POST'])
def ranked_shortlist():
    data = request.json
    job_id = data.get('job_id')
    candidates = data.get('candidates')
    
    if not job_id or not candidates:
        return jsonify({'error': 'Job ID and candidates are required.'}), 400
    
    ranked_list = shortlister.generate_shortlist(job_id, candidates)
    return jsonify(ranked_list), 200