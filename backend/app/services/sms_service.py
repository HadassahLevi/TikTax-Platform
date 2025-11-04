"""
SMS Service
Twilio integration for SMS verification
"""

from twilio.rest import Client
from ..core.config import settings
import random
import logging
from typing import Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# In-memory SMS code storage (Production: use Redis)
sms_codes: Dict[str, dict] = {}


class SMSService:
    """SMS service for sending and verifying SMS codes"""
    
    def __init__(self):
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        self.from_number = settings.TWILIO_PHONE_NUMBER
    
    def generate_code(self) -> str:
        """Generate 6-digit verification code"""
        return str(random.randint(100000, 999999))
    
    async def send_verification_code(self, phone_number: str) -> bool:
        """
        Send SMS verification code
        
        Args:
            phone_number: Phone number to send code to
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Generate and store code
            code = self.generate_code()
            sms_codes[phone_number] = {
                'code': code,
                'expires_at': datetime.utcnow() + timedelta(minutes=10),
                'attempts': 0
            }
            
            # Send SMS
            message = self.client.messages.create(
                body=f"קוד האימות שלך ב-Tik-Tax: {code}\nהקוד תקף ל-10 דקות.",
                from_=self.from_number,
                to=phone_number
            )
            
            logger.info(f"SMS sent to {phone_number}: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS to {phone_number}: {str(e)}")
            return False
    
    async def verify_code(self, phone_number: str, code: str) -> bool:
        """
        Verify SMS code
        
        Args:
            phone_number: Phone number to verify
            code: Verification code
            
        Returns:
            True if code is valid, False otherwise
        """
        stored_data = sms_codes.get(phone_number)
        
        if not stored_data:
            return False
        
        # Check expiration
        if datetime.utcnow() > stored_data['expires_at']:
            del sms_codes[phone_number]
            return False
        
        # Check attempts (max 3)
        if stored_data['attempts'] >= 3:
            del sms_codes[phone_number]
            return False
        
        # Verify code
        if stored_data['code'] == code:
            del sms_codes[phone_number]
            return True
        else:
            stored_data['attempts'] += 1
            return False


# Singleton instance
sms_service = SMSService()

