from datetime import datetime, timedelta
import random

class InterviewScheduler:
    def __init__(self):
        # Template messages for different communication types
        self.email_templates = {
            'invitation': '''
Dear {candidate_name},

We are pleased to inform you that your application for the {position} role has been shortlisted. 
We would like to invite you for an interview on {interview_date} at {interview_time}.

Please confirm your availability by clicking the link below:
{confirmation_link}

If this time doesn't work for you, please select an alternative slot:
{available_slots_link}

We look forward to meeting you!

Best regards,
{company_name} Recruitment Team
''',
            'confirmation': '''
Dear {candidate_name},

Thank you for confirming your interview for the {position} role on {interview_date} at {interview_time}.

Location: {interview_location}

Please bring your ID and a copy of your resume.

We look forward to meeting you!

Best regards,
{company_name} Recruitment Team
''',
            'reminder': '''
Dear {candidate_name},

This is a friendly reminder about your upcoming interview for the {position} role tomorrow at {interview_time}.

Location: {interview_location}

If you have any questions, please don't hesitate to contact us.

Best regards,
{company_name} Recruitment Team
'''
        }
    
    def schedule_interviews(self, shortlisted_candidates, available_slots, company_info):
        """
        Schedule interviews for shortlisted candidates
        
        Args:
            shortlisted_candidates (list): List of shortlisted candidates
            available_slots (list): Available interview time slots
            company_info (dict): Company information for templates
            
        Returns:
            dict: Interview schedule with candidate assignments
        """
        schedule = []
        
        for candidate in shortlisted_candidates:
            # In a real system, this would be more sophisticated,
            # potentially based on candidate preferences or availability
            if available_slots:
                # Assign a slot to this candidate
                slot = available_slots.pop(0)
                
                schedule.append({
                    "candidate": candidate,
                    "slot": slot,
                    "status": "scheduled",
                    "communication_history": []
                })
        
        return schedule
    
    def send_invitation(self, candidate, interview_details, company_info):
        """
        Generate and send interview invitation email
        
        Args:
            candidate (dict): Candidate information
            interview_details (dict): Interview date, time, etc.
            company_info (dict): Company information for templates
            
        Returns:
            dict: Result of the email sending operation
        """
        # In a real implementation, this would connect to an email service
        
        # Generate email content from template
        email_content = self.email_templates['invitation'].format(
            candidate_name=candidate["name"],
            position=interview_details["position"],
            interview_date=interview_details["date"],
            interview_time=interview_details["time"],
            confirmation_link=f"https://example.com/confirm/{interview_details['id']}",
            available_slots_link=f"https://example.com/reschedule/{interview_details['id']}",
            company_name=company_info["name"]
        )
        
        # Placeholder for email sending logic
        email_sent = True
        
        return {
            "success": email_sent,
            "message": "Invitation email sent" if email_sent else "Failed to send invitation",
            "timestamp": datetime.now().isoformat()
        }
    
    def send_reminder(self, candidate, interview_details, company_info):
        """Send reminder email before interview"""
        # Similar implementation as send_invitation
        # Would be called by a scheduled task
        pass
    
    def process_confirmation(self, confirmation_id, status):
        """Process candidate's confirmation response"""
        # In a real system, this would update the interview status in the database
        pass