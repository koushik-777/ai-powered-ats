import unittest
from src.agents.interview_scheduler.scheduler import InterviewScheduler

class TestInterviewScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = InterviewScheduler()

    def test_schedule_interview(self):
        candidate_email = "candidate@example.com"
        interview_time = "2023-10-01 10:00:00"
        result = self.scheduler.schedule_interview(candidate_email, interview_time)
        self.assertTrue(result)

    def test_send_invitation(self):
        candidate_email = "candidate@example.com"
        interview_time = "2023-10-01 10:00:00"
        result = self.scheduler.send_invitation(candidate_email, interview_time)
        self.assertTrue(result)

    def test_invalid_schedule(self):
        candidate_email = "invalid_email"
        interview_time = "2023-10-01 10:00:00"
        with self.assertRaises(ValueError):
            self.scheduler.schedule_interview(candidate_email, interview_time)

if __name__ == '__main__':
    unittest.main()