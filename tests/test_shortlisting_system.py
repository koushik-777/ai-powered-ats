import unittest
from src.agents.shortlisting_system.shortlister import Shortlister

class TestShortlistingSystem(unittest.TestCase):

    def setUp(self):
        self.shortlister = Shortlister()

    def test_filter_candidates(self):
        candidates = [
            {'name': 'Alice', 'match_score': 85},
            {'name': 'Bob', 'match_score': 75},
            {'name': 'Charlie', 'match_score': 90}
        ]
        threshold = 80
        expected_shortlist = [{'name': 'Alice', 'match_score': 85}, {'name': 'Charlie', 'match_score': 90}]
        actual_shortlist = self.shortlister.filter_candidates(candidates, threshold)
        self.assertEqual(actual_shortlist, expected_shortlist)

    def test_generate_shortlist(self):
        candidates = [
            {'name': 'Alice', 'match_score': 85},
            {'name': 'Bob', 'match_score': 75},
            {'name': 'Charlie', 'match_score': 90}
        ]
        expected_ranked_shortlist = [
            {'name': 'Charlie', 'match_score': 90},
            {'name': 'Alice', 'match_score': 85}
        ]
        actual_ranked_shortlist = self.shortlister.generate_shortlist(candidates)
        self.assertEqual(actual_ranked_shortlist, expected_ranked_shortlist)

if __name__ == '__main__':
    unittest.main()