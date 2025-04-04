from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_restful import Api
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email configuration
EMAIL_SENDER = ""  # Your Gmail address
EMAIL_PASSWORD = ""    # App password (not your regular password)
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587

# Try to import your agents, with fallback for testing
try:
    from agents.cv_parser.parser import CVParser
    from agents.job_description_summarizer.summarizer import JobDescriptionSummarizer
    from agents.matching_algorithm.matcher import Matcher
    from agents.shortlisting_system.shortlister import Shortlister
    from agents.interview_scheduler.scheduler import InterviewScheduler
    from database.db_manager import DBManager
except ImportError:
    # Mock implementations for testing or when modules aren't fully implemented
    class CVParser:
        def parse(self, file_path):
            return {"skills": ["Python", "Flask", "React"], "experience": "5 years"}
        
        def standardize_data(self, data):
            return data
            
        def calculate_score(self, data):
            return 85
    
    class JobDescriptionSummarizer:
        def extract_key_elements(self, text):
            return {
                "skills": ["Python", "Flask", "React", "JavaScript"],
                "experience": "3+ years",
                "education": "Bachelor's degree"
            }
            
        def summarize(self, text):
            return "This job requires a skilled developer with Python experience."
    
    class Matcher:
        def calculate_match(self, cv_data, job_data):
            return 75.5
            
        def generate_match_report(self, cv_data, job_data):
            return {
                "overall_score": 75.5,
                "skills_match": 80,
                "experience_match": 70,
                "education_match": 90
            }
    
    class Shortlister:
        def filter_candidates(self, job_id, candidates):
            return candidates[:5]
            
        def generate_shortlist(self, job_id, candidates):
            return [{"id": c["id"], "name": c["name"], "score": 85 - i*5} for i, c in enumerate(candidates[:5])]
    
    class InterviewScheduler:
        def schedule_interview(self, candidate_id, job_id, date_time):
            return {"id": 1, "candidate_id": candidate_id, "job_id": job_id, "date_time": date_time}
        
        def send_invitation(self, candidate, interview_details, company_info):
            return f"Invitation email for {candidate['name']} to interview for {interview_details['position']} at {company_info['name']}."

    class DBManager:
        def __init__(self):
            self.db_path = "recruitment.db"
            print(f"Database initialized at {self.db_path}")

app = Flask(__name__)
CORS(app)
api = Api(app)

# Initialize components
cv_parser = CVParser()
job_summarizer = JobDescriptionSummarizer()
matcher = Matcher()
shortlister = Shortlister()
interview_scheduler = InterviewScheduler()
db_manager = DBManager()

# In-memory data storage for demo
JOBS = [
    {
        'id': 1,
        'title': 'Software Engineer',
        'company': 'Tech Solutions Inc.',
        'description': '''
        Required Skills:
        - Proficiency in programming languages such as Java, Python, or C++
        - Experience with web development frameworks (e.g., React, Angular)
        - Strong understanding of database management systems (e.g., MySQL, PostgreSQL)
        - Familiarity with version control systems (e.g., Git)
        - Excellent communication and teamwork skills
        ''',
        'candidates_count': 0
    },
    {
        'id': 2,
        'title': 'Data Scientist',
        'company': 'Data Insights Corp.',
        'description': '''
        Required Skills:
        - Proficiency in Python, R, or similar languages
        - Experience with machine learning libraries (TensorFlow, PyTorch, scikit-learn)
        - Strong understanding of statistical methods and algorithms
        - Data visualization skills (Tableau, Power BI)
        - SQL and database knowledge
        ''',
        'candidates_count': 0
    }
]

CANDIDATES = []
INTERVIEWS = []

# Serve UI files
@app.route('/')
def index():
    return send_from_directory('../ui/public', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('../ui/public', path)
    except:
        # If file not found in ui/public, try src/ui
        try:
            return send_from_directory('../src/ui', path)
        except:
            return "File not found", 404

# API endpoints
@app.route('/api/interviews', methods=['GET'])
def get_interviews():
    return jsonify(INTERVIEWS), 200

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    return jsonify(JOBS), 200

@app.route('/api/analyze-job', methods=['POST'])
def analyze_job():
    if not request.json or 'description' not in request.json:
        return jsonify({'error': 'No job description provided'}), 400
    
    job_description = request.json['description']
    job_title = request.json.get('title', 'Untitled Job')
    company = request.json.get('company', 'Unknown Company')
    
    # Process the job description
    try:
        key_elements = job_summarizer.extract_key_elements(job_description)
        summary = job_summarizer.summarize(job_description)
        
        # Add to in-memory storage
        job_id = len(JOBS) + 1
        new_job = {
            'id': job_id,
            'title': job_title,
            'company': company,
            'description': job_description,
            'candidates_count': 0
        }
        JOBS.append(new_job)
        
        return jsonify({
            'message': 'Job analyzed successfully',
            'job_id': job_id,
            'title': job_title,
            'company': company,
            'key_elements': key_elements,
            'summary': summary
        }), 200
    except Exception as e:
        print(f"Error analyzing job: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/parse-cv', methods=['POST'])
def parse_cv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    job_id = request.form.get('job_id', '')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save the file with a secure filename to avoid path traversal
        import os
        from werkzeug.utils import secure_filename
        
        temp_dir = os.path.join('data', 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        file_path = os.path.join(temp_dir, secure_filename(file.filename))
        file.save(file_path)
        
        # Parse the CV
        cv_parser = CVParser()
        cv_data = cv_parser.parse(file_path)
        
        # Add to candidates list if not already there
        candidate_id = len(CANDIDATES) + 1
        candidate = {
            'id': candidate_id,
            'name': name,
            'email': email,
            'phone': phone,
            'job_id': int(job_id) if job_id else None,
            'extracted_skills': ', '.join(cv_data.get('skills', [])),
            'score': cv_data.get('score', 0),
            'recommendation': cv_data.get('recommendation', '')
        }
        CANDIDATES.append(candidate)
        
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Build response
        response = {
            'message': 'CV parsed successfully',
            'extracted_data': cv_data
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        import traceback
        print(f"Error in parse_cv: {str(e)}")
        print(traceback.format_exc())  # Print the full traceback
        return jsonify({'error': f'An error occurred while processing the CV: {str(e)}'}), 500

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    return jsonify(CANDIDATES)

@app.route('/api/schedule-interview', methods=['POST'])
def schedule_interview():
    data = request.json
    
    # Validate request data
    required_fields = ['candidate_name', 'job_id', 'scheduled_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        # Create the interview record
        interview_id = len(INTERVIEWS) + 1
        
        # Find the related job
        job = next((j for j in JOBS if j.get('id') == data['job_id']), None)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Create interview object
        interview = {
            'id': interview_id,
            'candidate_name': data['candidate_name'],
            'candidate_email': data.get('candidate_email', ''),
            'job_id': data['job_id'],
            'job_title': job.get('title', 'Unknown Position'),
            'company': job.get('company', 'Unknown Company'),
            'scheduled_date': data['scheduled_date'],
            'status': 'scheduled'
        }
        
        # Add to interviews list
        INTERVIEWS.append(interview)
        
        # Increment the candidates_count for the job
        job['candidates_count'] += 1
        
        # Send email notification if requested
        email_sent = False
        if data.get('send_email', False) and interview['candidate_email']:
            email_sent = send_interview_email(
                interview['candidate_name'],
                interview['candidate_email'],
                interview['job_title'],
                interview['company'],
                interview['scheduled_date']
            )
            
            # Update interview with email status
            interview['email_sent'] = email_sent
        
        return jsonify({
            'message': 'Interview scheduled successfully',
            'interview': interview,
            'email_sent': email_sent
        }), 201
    
    except Exception as e:
        print(f"Error scheduling interview: {str(e)}")
        return jsonify({'error': f'Failed to schedule interview: {str(e)}'}), 500

@app.route('/api/shortlist', methods=['POST'])
def shortlist_candidates():
    data = request.json
    job_id = data.get('job_id')
    threshold = data.get('threshold', 70)  # Default threshold is 70
    
    if not job_id:
        return jsonify({'error': 'Job ID is required'}), 400
    
    try:
        # Get all candidates for this job
        job_candidates = [c for c in CANDIDATES if c.get('job_id') == job_id]
        
        # Filter candidates based on score threshold
        shortlisted = [c for c in job_candidates if c.get('score', 0) >= threshold]
        
        # Sort by score (highest first)
        shortlisted.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return jsonify({
            'message': f'Successfully shortlisted {len(shortlisted)} candidates',
            'shortlisted': shortlisted
        }), 200
    
    except Exception as e:
        print(f"Error shortlisting candidates: {e}")
        return jsonify({'error': str(e)}), 500

def send_interview_email(candidate_name, candidate_email, job_title, company, scheduled_date):
    """Send an email to the candidate about their scheduled interview"""
    if not candidate_email:
        print("No email address provided, skipping email notification")
        return False
    
    # Parse the scheduled date
    try:
        date_obj = datetime.strptime(scheduled_date, '%Y-%m-%dT%H:%M:%S')
        formatted_date = date_obj.strftime('%A, %B %d, %Y')
        formatted_time = date_obj.strftime('%I:%M %p')
    except:
        formatted_date = scheduled_date.split('T')[0]
        formatted_time = scheduled_date.split('T')[1]
    
    # Email content
    subject = f"Interview Invitation: {job_title} at {company}"
    
    # Create HTML email body
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #4a86e8;">Interview Invitation</h2>
            <p>Dear {candidate_name},</p>
            
            <p>We are pleased to invite you for an interview for the <strong>{job_title}</strong> position at <strong>{company}</strong>.</p>
            
            <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #4a86e8; margin: 20px 0;">
                <h3 style="margin-top: 0;">Interview Details:</h3>
                <p><strong>Date:</strong> {formatted_date}</p>
                <p><strong>Time:</strong> {formatted_time}</p>
                <p><strong>Company:</strong> {company}</p>
            </div>
            
            <p>Please confirm your attendance by replying to this email. If you need to reschedule, please let us know as soon as possible.</p>
            
            <p>Best regards,<br>
            HR Team<br>
            {company}</p>
        </div>
    </body>
    </html>
    """
    
    # Plain text alternative
    text_body = f"""
    Interview Invitation
    
    Dear {candidate_name},
    
    We are pleased to invite you for an interview for the {job_title} position at {company}.
    
    Interview Details:
    Date: {formatted_date}
    Time: {formatted_time}
    Company: {company}
    
    Please confirm your attendance by replying to this email. If you need to reschedule, 
    please let us know as soon as possible.
    
    Best regards,
    HR Team
    {company}
    """
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = candidate_email
        
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"Email sent successfully to {candidate_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)
