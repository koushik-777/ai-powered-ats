import unittest
from src.agents.cv_parser.parser import CVParser

class TestCVParser(unittest.TestCase):

    def setUp(self):
        self.parser = CVParser()

    def test_parse_cv_valid(self):
        # Assuming we have a valid CV file path for testing
        cv_file_path = 'data/sample_resumes/example1.pdf'
        result = self.parser.parse_cv(cv_file_path)
        self.assertIsInstance(result, dict)
        self.assertIn('education', result)
        self.assertIn('work_experience', result)
        self.assertIn('skills', result)

    def test_extract_information(self):
        sample_cv_data = {
            'name': 'John Doe',
            'education': 'Bachelor of Science in Computer Science',
            'work_experience': 'Software Engineer at Company X',
            'skills': ['Python', 'NLP', 'Machine Learning']
        }
        extracted_info = self.parser.extract_information(sample_cv_data)
        self.assertEqual(extracted_info['name'], 'John Doe')
        self.assertEqual(extracted_info['education'], 'Bachelor of Science in Computer Science')
        self.assertEqual(extracted_info['work_experience'], 'Software Engineer at Company X')
        self.assertIn('Python', extracted_info['skills'])

if __name__ == '__main__':
    unittest.main()