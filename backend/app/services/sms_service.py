"""
SMS Service
Twilio integration for SMS verification
"""


class SMSService:
    """SMS service using Twilio"""
    
    @staticmethod
    def send_verification_code(phone: str, code: str) -> None:
        """
        Send SMS verification code
        
        Args:
            phone: Phone number (Israeli format: +972...)
            code: Verification code
        """
        # TODO: Implement Twilio SMS sending
        pass
    
    @staticmethod
    def generate_verification_code() -> str:
        """
        Generate 6-digit verification code
        
        Returns:
            Verification code
        """
        import random
        return str(random.randint(100000, 999999))
