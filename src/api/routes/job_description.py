from flask import Blueprint, request, jsonify
from src.agents.job_description_summarizer.summarizer import JobDescriptionSummarizer

job_description_bp = Blueprint('job_description', __name__)
summarizer = JobDescriptionSummarizer()

@job_description_bp.route('/summarize', methods=['POST'])
def summarize_job_description():
    data = request.json
    job_description = data.get('job_description', '')
    
    if not job_description:
        return jsonify({'error': 'Job description is required'}), 400
    
    summary = summarizer.summarize(job_description)
    return jsonify(summary), 200

@job_description_bp.route('/extract', methods=['POST'])
def extract_key_elements():
    data = request.json
    job_description = data.get('job_description', '')
    
    if not job_description:
        return jsonify({'error': 'Job description is required'}), 400
    
    key_elements = summarizer.extract_key_elements(job_description)
    return jsonify(key_elements), 200