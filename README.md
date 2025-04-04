# AI Recruitment System

## Overview
The AI Recruitment System is a multi-agentic AI solution designed to automate and enhance the recruitment process. It matches candidates to job descriptions, shortlists qualified applicants, and streamlines the interview scheduling process.

## Components
The system consists of the following main components:

1. **Job Description Summarizer**: An NLP model that extracts and summarizes key elements from job descriptions, including required skills, experience, qualifications, and responsibilities.

2. **CV/Resume Parser and Analyzer**: An AI model that extracts relevant information from CVs in various formats, standardizing the data for further analysis.

3. **Matching Algorithm**: A sophisticated algorithm that compares CV data against job requirements, generating match percentages and qualification mappings.

4. **Candidate Shortlisting System**: A filtering system that ranks candidates based on match scores and generates shortlists with justifications for selection.

5. **Interview Scheduler**: An automated system that communicates with shortlisted candidates, sends interview invitations, and manages scheduling.

## Technical Requirements
- Built using a multi-agent framework for coordination between components.
- Utilizes an SQLite database for persistent storage and retrieval.
- Ensures data privacy compliance and secure handling of personal information.
- Features a user-friendly interface for HR personnel to review results.
- Includes logging and monitoring systems for performance evaluation.

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd ai-recruitment-system
pip install -r requirements.txt
```

## Usage
Run the application using the following command:

```bash
python src/main.py
```

Access the user interface through your web browser at `http://localhost:8000`.

## Testing
Unit tests are provided for each component of the system. To run the tests, use:

```bash
pytest tests/
```

## Documentation
For detailed API documentation, system architecture, and algorithm bias analysis, refer to the `docs` directory.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.