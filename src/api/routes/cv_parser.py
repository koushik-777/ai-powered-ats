from flask import Blueprint, request, jsonify
from agents.cv_parser.parser import CVParser

cv_parser_bp = Blueprint('cv_parser', __name__)
cv_parser = CVParser()

@cv_parser_bp.route('/parse_cv', methods=['POST'])
def parse_cv():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    
    try:
        cv_data = cv_parser.parse_cv(file)
        return jsonify(cv_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cv_parser_bp.route('/extract_information', methods=['POST'])
def extract_information():
    cv_text = request.json.get('cv_text')
    if not cv_text:
        return jsonify({'error': 'No CV text provided'}), 400
    
    try:
        information = cv_parser.extract_information(cv_text)
        return jsonify(information), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500