# API Documentation for AI Recruitment System

## Overview
This document provides an overview of the API endpoints available in the AI Recruitment System. The API is designed to facilitate interactions with various components of the recruitment process, including job description summarization, CV parsing, candidate matching, shortlisting, and interview scheduling.

## Base URL
The base URL for the API is: `http://localhost:5000/api`

## Endpoints

### Job Description API
- **Endpoint:** `/job_description/summarize`
  - **Method:** POST
  - **Description:** Summarizes a job description and extracts key elements.
  - **Request Body:**
    ```json
    {
      "job_description": "string"
    }
    ```
  - **Response:**
    ```json
    {
      "summary": "string",
      "key_elements": {
        "skills": ["string"],
        "experience": "string",
        "qualifications": "string",
        "responsibilities": "string"
      }
    }
    ```

### CV Parser API
- **Endpoint:** `/cv_parser/parse`
  - **Method:** POST
  - **Description:** Parses a CV and extracts relevant information.
  - **Request Body:**
    ```json
    {
      "cv_file": "base64_encoded_string"
    }
    ```
  - **Response:**
    ```json
    {
      "education": ["string"],
      "work_experience": ["string"],
      "skills": ["string"],
      "certifications": ["string"]
    }
    ```

### Matching Algorithm API
- **Endpoint:** `/matching/compare`
  - **Method:** POST
  - **Description:** Compares CV data against job requirements and generates a match percentage.
  - **Request Body:**
    ```json
    {
      "cv_data": {
        "skills": ["string"],
        "experience": "string",
        "qualifications": "string"
      },
      "job_requirements": {
        "skills": ["string"],
        "experience": "string",
        "qualifications": "string"
      }
    }
    ```
  - **Response:**
    ```json
    {
      "match_percentage": "number",
      "details": {
        "matched_skills": ["string"],
        "missing_skills": ["string"]
      }
    }
    ```

### Shortlisting API
- **Endpoint:** `/shortlisting/filter`
  - **Method:** POST
  - **Description:** Filters candidates based on match scores and generates a ranked shortlist.
  - **Request Body:**
    ```json
    {
      "candidates": [
        {
          "cv_data": {
            "skills": ["string"],
            "experience": "string",
            "qualifications": "string"
          },
          "match_score": "number"
        }
      ],
      "threshold": "number"
    }
    ```
  - **Response:**
    ```json
    {
      "shortlisted_candidates": [
        {
          "cv_data": "object",
          "match_score": "number"
        }
      ]
    }
    ```

### Interview Scheduling API
- **Endpoint:** `/scheduling/schedule`
  - **Method:** POST
  - **Description:** Schedules an interview and sends an invitation to the candidate.
  - **Request Body:**
    ```json
    {
      "candidate_email": "string",
      "interview_time": "string",
      "interview_details": "string"
    }
    ```
  - **Response:**
    ```json
    {
      "status": "string",
      "message": "string"
    }
    ```

## Error Handling
All API responses include an error message in the event of a failure. The error response format is as follows:
```json
{
  "error": {
    "code": "string",
    "message": "string"
  }
}
```

## Conclusion
This API documentation outlines the key endpoints available in the AI Recruitment System. For further details on implementation or usage, please refer to the source code or contact the development team.