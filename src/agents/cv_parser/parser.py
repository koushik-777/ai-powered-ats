import re
import chardet
import io

class CVParser:
    def __init__(self):
        self.supported_formats = ["pdf", "docx", "txt"]
    
    def parse(self, cv_file_path):
        """Parse a CV/resume file and extract relevant information"""
        # Extract file extension
        file_extension = cv_file_path.split('.')[-1].lower()
        
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}. Supported formats: {', '.join(self.supported_formats)}")
        
        # Extract content based on file type
        content = ""
        try:
            if file_extension == 'pdf':
                content = self._extract_text_from_pdf(cv_file_path)
            elif file_extension == 'docx':
                content = self._extract_text_from_docx(cv_file_path)
            else:  # txt or other text formats
                content = self._extract_text_from_txt(cv_file_path)
            
            # Clean up and normalize the text
            content = self._preprocess_text(content)
            
            # Debug: Print a sample of the extracted content
            print(f"---Sample CV content (first 300 chars):---")
            print(content[:300])
            print("---End of sample---")
            
        except Exception as e:
            print(f"Error during content extraction: {e}")
            return {
                "skills": [],
                "work_experience": ["Error processing file: " + str(e)],
                "education": [],
                "score": 0,
                "recommendation": "Error processing file"
            }
        
        try:
            # Extract information from the content
            skills = self._extract_skills(content)
            work_experience = self._extract_work_experience(content)
            education = self._extract_education(content)
            
            # Standardize and calculate score
            extracted_data = {
                "skills": skills,
                "work_experience": work_experience,
                "education": education
            }
            standardized_data = self.standardize_data(extracted_data)
            score = self.calculate_score(standardized_data)
            recommendation = self.get_recommendation(score)
            
            # Include score and recommendation in the final output
            extracted_data["score"] = score
            extracted_data["recommendation"] = recommendation
            
            return extracted_data
        except Exception as e:
            print(f"Error during data extraction or scoring: {e}")
            return {
                "skills": [],
                "work_experience": ["Error processing file: " + str(e)],
                "education": [],
                "score": 0,
                "recommendation": "Error processing file"
            }
    
    def _extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file"""
        try:
            # Try to import PyPDF2
            from PyPDF2 import PdfReader
            
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
                
            # If text is empty, try another method
            if not text.strip():
                raise ImportError("PyPDF2 extracted empty text")
                
            return text
        except ImportError:
            # Fall back to pdfminer if PyPDF2 is not available
            try:
                from pdfminer.high_level import extract_text
                return extract_text(pdf_path)
            except ImportError:
                with open(pdf_path, 'rb') as file:
                    return f"PDF file detected, but no PDF parser library installed. Consider installing PyPDF2 or pdfminer.six."
    
    def _extract_text_from_docx(self, docx_path):
        """Extract text from a DOCX file"""
        try:
            import docx
            doc = docx.Document(docx_path)
            return " ".join(paragraph.text for paragraph in doc.paragraphs)
        except ImportError:
            with open(docx_path, 'rb') as file:
                return f"DOCX file detected, but python-docx library not installed. Consider installing python-docx."
    
    def _extract_text_from_txt(self, txt_path):
        """Extract text from a TXT file with robust encoding detection"""
        with open(txt_path, 'rb') as file:
            raw_data = file.read()
            
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252']
        content = None
        
        # First try chardet
        detected_encoding = chardet.detect(raw_data)['encoding']
        if detected_encoding:
            encodings.insert(0, detected_encoding)
        
        # Try each encoding until one works
        for encoding in encodings:
            try:
                content = raw_data.decode(encoding)
                return content
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail, use latin-1 as a fallback since it can decode any byte
        return raw_data.decode('latin-1', errors='replace')
    
    def _extract_skills(self, content):
        """Extract skills from the CV content"""
        # Example skill keywords
        skill_keywords = [
            "Python", "Java", "C++", "JavaScript", "React", "Angular", "SQL",
            "Machine Learning", "Data Analysis", "AWS", "Docker", "Kubernetes"
        ]
        skills = [skill for skill in skill_keywords if skill.lower() in content.lower()]
        return skills
    
    def _extract_work_experience(self, content):
        """Extract work experience from the CV content"""
        # Check for work experience section headers
        work_headers = [
            r'(?i)(?:^|\n\n)(WORK EXPERIENCE|EXPERIENCE|EMPLOYMENT|PROFESSIONAL EXPERIENCE|WORK HISTORY)(.+?)(?=\n\n[A-Z\s]{2,}:|$)',
            r'(?i)(?:^|\n)(WORK|PROFESSIONAL|EMPLOYMENT)[:\n](.+?)(?=\n[A-Z\s]{2,}:|$)'
        ]
        
        section_content = ""
        for pattern in work_headers:
            matches = re.search(pattern, content, re.DOTALL)
            if matches:
                section_content = matches.group(0)
                break
        
        if not section_content:
            section_content = content
        
        # Extract job titles, companies, and dates
        job_patterns = [
            r'(?i)([A-Z][A-Za-z\s&.,]+)\s*[-–—|]\s*([^\n]+)',  # Company - Position
            r'(?i)(Data Scientist|Software Engineer|Developer|Programmer|Analyst|Manager|Director|Specialist|Consultant)[^\n]*(?:at|with|for)?\s*([^\n]+)',  # Position at Company
            r'(?i)(\d{4}\s*[-–—to]+\s*\d{4}|\d{4}\s*[-–—to]+\s*present|\d{4}\s*[-–—to]+\s*current)'  # Date ranges
        ]
        
        work_experience = []
        
        # Check job patterns
        for pattern in job_patterns:
            matches = re.findall(pattern, section_content)
            for match in matches:
                if isinstance(match, tuple):
                    job_info = ' - '.join([part.strip() for part in match if part and len(part.strip()) > 0])
                    work_experience.append(job_info)
        
        # Remove duplicates and clean up
        work_experience = list(set(work_experience))
        work_experience = [exp.strip() for exp in work_experience if len(exp.strip()) > 10]
        
        return work_experience if work_experience else ["No work experience detected"]
    
    def _extract_education(self, content):
        """Extract education details from the CV content"""
        # First try to extract sections - look for headers
        education_patterns = [
            r'(?i)(?:^|\n\n)(EDUCATION|ACADEMIC BACKGROUND|EDUCATIONAL QUALIFICATIONS?)(.+?)(?=\n\n[A-Z\s]{2,}:|$)',
            r'(?i)(?:^|\n)(EDUCATION|ACADEMIC|QUALIFICATION)S?[:\n](.+?)(?=\n[A-Z\s]{2,}:|$)'
        ]
        
        section_content = ""
        for pattern in education_patterns:
            matches = re.search(pattern, content, re.DOTALL)
            if matches:
                section_content = matches.group(0)
                break
        
        if not section_content:
            section_content = content
        
        # Extract degrees and institutions
        degree_patterns = [
            r"(?i)(B\.?Tech|Bachelor[\"']?s?|B\.?A|B\.?S|B\.?E)[^\n]*(in|of)?[^\n]*?([A-Za-z\s&]+)",
            r'(?i)(M\.?Tech|Master[\'"]?s?|M\.?A|M\.?S|MBA)[^\n]*(in|of)?[^\n]*?([A-Za-z\s&]+)',
            r'(?i)(Ph\.?D|Doctorate)[^\n]*(in|of)?[^\n]*?([A-Za-z\s&]+)'
        ]
        
        institute_patterns = [
            r'(?i)([A-Z][A-Za-z\s]+(?:University|College|Institute|School))',
            r'(?i)(University|College|Institute|School)\s+of\s+([A-Za-z\s]+)'
        ]
        
        education_info = []
        
        # Extract degrees
        for pattern in degree_patterns:
            matches = re.findall(pattern, section_content)
            for match in matches:
                if isinstance(match, tuple):
                    degree = ' '.join([part for part in match if part and len(part.strip()) > 0])
                    education_info.append(degree.strip())
        
        # Extract institutions
        for pattern in institute_patterns:
            matches = re.findall(pattern, section_content)
            for match in matches:
                if isinstance(match, tuple):
                    institute = ' '.join([part for part in match if part and len(part.strip()) > 0])
                    education_info.append(institute.strip())
                else:
                    education_info.append(match.strip())
        
        # Remove duplicates and clean up
        education_info = list(set(education_info))
        education_info = [edu.strip() for edu in education_info if len(edu.strip()) > 5]
        
        return education_info if education_info else ["No education details detected"]
    
    def standardize_data(self, extracted_data):
        """
        Standardize extracted data to a consistent format
        
        Args:
            extracted_data (dict): Data extracted from the CV
            
        Returns:
            dict: Standardized data
        """
       
        if "skills" in extracted_data:
            extracted_data["skills"] = [skill.lower() for skill in extracted_data["skills"]]
        return extracted_data
    
    def calculate_score(self, standardized_data):
        """
        Calculate a score for the CV based on extracted data
        
        Args:
            standardized_data (dict): Standardized CV data
            
        Returns:
            int: A score representing the quality of the CV
        """
        score = 0
        if "skills" in standardized_data:
            score += len(standardized_data["skills"]) * 10  # 10 points per skill
        if "work_experience" in standardized_data:
            score += len(standardized_data["work_experience"]) * 5  # 5 points per work experience entry
        if "education" in standardized_data:
            score += len(standardized_data["education"]) * 5  # 5 points per education entry
        
        return min(score, 100)  # Cap the score at 100
    
    def _preprocess_text(self, text):
        """Clean and normalize text for better extraction"""
        # Fix spacing issues (common in PDF extraction)
        text = re.sub(r'([a-z])[\s]([A-Z])', r'\1 \2', text)  # Add space between mixed case
        text = re.sub(r'([a-zA-Z])[\s]([a-z])', r'\1\2', text)  # Remove spaces between letters
        
        # Normalize newlines
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove bullet points and special characters
        text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219•▪●■○▸▶]', '', text)  # Common bullet points
        text = re.sub(r'[^a-zA-Z0-9\s.,:;\'"-]', '', text)  # Remove special characters except common punctuation
        
        # Fix common OCR/extraction artifacts
        text = re.sub(r'([A-Za-z])(\s+)(-)', r'\1-', text)  # Fix "word - word" spacing
        text = re.sub(r'(\d)(\s+)(years?)', r'\1 \3', text)  # Fix "5 years" spacing
        
        return text.strip()
    
    def get_recommendation(self, score):
        """
        Provide a recommendation based on the CV score
        
        Args:
            score (int): The calculated CV score
            
        Returns:
            str: Recommendation message
        """
        if score >= 70:
            return "Eligible to apply for the job"
        elif score >= 50:
            return "Consider applying, but improvements are recommended"
        else:
            return "Not eligible to apply for the job"