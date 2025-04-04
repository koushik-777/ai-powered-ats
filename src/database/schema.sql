-- Schema for AI Recruitment System Database

-- Job Descriptions Table
CREATE TABLE IF NOT EXISTS job_descriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    description TEXT NOT NULL,
    extracted_skills TEXT,
    extracted_qualifications TEXT,
    extracted_experience TEXT,
    extracted_responsibilities TEXT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Candidates Table
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    cv_file_path TEXT NOT NULL,
    extracted_skills TEXT,
    extracted_qualifications TEXT,
    extracted_experience TEXT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Candidate-Job Matches Table
CREATE TABLE IF NOT EXISTS candidate_job_matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    match_score REAL NOT NULL,
    match_details TEXT,
    is_shortlisted BOOLEAN DEFAULT FALSE,
    shortlisting_justification TEXT,
    date_matched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates (id),
    FOREIGN KEY (job_id) REFERENCES job_descriptions (id)
);

-- Interviews Table
CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_job_match_id INTEGER NOT NULL,
    scheduled_date DATETIME NOT NULL,
    location TEXT,
    interviewer TEXT,
    status TEXT DEFAULT 'scheduled',
    notes TEXT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_job_match_id) REFERENCES candidate_job_matches (id)
);

-- Communications Table
CREATE TABLE IF NOT EXISTS communications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
);

-- Users Table (for system users like HR personnel)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_candidate_job_matches_candidate_id ON candidate_job_matches (candidate_id);
CREATE INDEX IF NOT EXISTS idx_candidate_job_matches_job_id ON candidate_job_matches (job_id);
CREATE INDEX IF NOT EXISTS idx_interviews_match_id ON interviews (candidate_job_match_id);
CREATE INDEX IF NOT EXISTS idx_communications_candidate_id ON communications (candidate_id);