import unittest
from src.agents.matching_algorithm.matcher import Matcher

class TestMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = Matcher()

    def test_compare_exact_match(self):
        cv_data = {
            'skills': ['Python', 'Machine Learning', 'Data Analysis'],
            'experience': 5,
            'education': 'Master\'s Degree'
        }
        job_requirements = {
            'required_skills': ['Python', 'Machine Learning'],
            'preferred_skills': ['Data Analysis'],
            'min_experience': 3,
            'education': 'Master\'s Degree'
        }
        match_score = self.matcher.compare(cv_data, job_requirements)
        self.assertEqual(match_score, 100)

    def test_compare_partial_match(self):
        cv_data = {
            'skills': ['Python', 'Data Analysis'],
            'experience': 2,
            'education': 'Bachelor\'s Degree'
        }
        job_requirements = {
            'required_skills': ['Python', 'Machine Learning'],
            'preferred_skills': ['Data Analysis'],
            'min_experience': 3,
            'education': 'Master\'s Degree'
        }
        match_score = self.matcher.compare(cv_data, job_requirements)
        self.assertLess(match_score, 100)

    def test_generate_match_percentage(self):
        match_score = 85
        percentage = self.matcher.generate_match_percentage(match_score)
        self.assertEqual(percentage, 85)

if __name__ == '__main__':
    unittest.main()