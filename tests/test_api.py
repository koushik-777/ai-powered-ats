import unittest
from src.api.routes.job_description import summarize_job_description
from src.api.routes.cv_parser import parse_cv
from src.api.routes.matching import match_candidates
from src.api.routes.shortlisting import shortlist_candidates
from src.api.routes.scheduling import schedule_interview

class TestAPI(unittest.TestCase):

    def test_summarize_job_description(self):
        response = summarize_job_description({"description": "Sample job description"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("key_elements", response.json)

    def test_parse_cv(self):
        response = parse_cv({"cv": "Sample CV content"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("extracted_information", response.json)

    def test_match_candidates(self):
        response = match_candidates({"job_requirements": "Sample requirements", "cvs": ["Sample CV content"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn("match_results", response.json)

    def test_shortlist_candidates(self):
        response = shortlist_candidates({"match_scores": [0.85, 0.75]})
        self.assertEqual(response.status_code, 200)
        self.assertIn("shortlisted_candidates", response.json)

    def test_schedule_interview(self):
        response = schedule_interview({"candidate_id": 1, "time_slot": "2023-10-01T10:00:00"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("confirmation", response.json)

if __name__ == '__main__':
    unittest.main()