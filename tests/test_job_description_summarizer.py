import unittest
from src.agents.job_description_summarizer.summarizer import JobDescriptionSummarizer

class TestJobDescriptionSummarizer(unittest.TestCase):

    def setUp(self):
        self.summarizer = JobDescriptionSummarizer()

    def test_extract_key_elements(self):
        job_description = "We are looking for a software engineer with experience in Python and machine learning."
        expected_output = {
            'skills': ['Python', 'machine learning'],
            'experience': 'software engineer',
            'qualifications': None,
            'responsibilities': None
        }
        self.assertEqual(self.summarizer.extract_key_elements(job_description), expected_output)

    def test_summarize(self):
        job_description = "We are looking for a software engineer with experience in Python and machine learning."
        expected_summary = "Software engineer with experience in Python and machine learning."
        self.assertEqual(self.summarizer.summarize(job_description), expected_summary)

if __name__ == '__main__':
    unittest.main()