"""
Email Service
SendGrid integration for email notifications
"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Email service using SendGrid"""
    
    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.from_email = settings.SENDGRID_FROM_EMAIL
    
    async def send_password_reset_email(self, to_email: str, user_name: str, reset_token: str) -> bool:
        """
        Send password reset email
        
        Args:
            to_email: Recipient email address
            user_name: User's full name
            reset_token: Password reset token
            
        Returns:
            True if sent successfully, False otherwise
        """
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        html_content = f"""
        <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>שלום {user_name},</h2>
            <p>קיבלנו בקשה לאיפוס הסיסמה שלך ב-Tik-Tax.</p>
            <p>לחץ על הקישור הבא כדי לאפס את הסיסמה:</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background-color: #2563EB; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 6px; display: inline-block;">
                    אפס סיסמה
                </a>
            </p>
            <p>הקישור תקף למשך שעה.</p>
            <p style="color: #6B7280; font-size: 14px;">
                אם לא ביקשת לאפס את הסיסמה, התעלם ממייל זה.
            </p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #E5E7EB;">
            <p style="color: #9CA3AF; font-size: 12px;">
                בברכה,<br>צוות Tik-Tax
            </p>
        </div>
        """
        
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject='איפוס סיסמה - Tik-Tax',
            html_content=html_content
        )
        
        try:
            response = self.client.send(message)
            logger.info(f"Password reset email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    async def send_welcome_email(self, to_email: str, user_name: str) -> bool:
        """
        Send welcome email to new users
        
        Args:
            to_email: Recipient email address
            user_name: User's full name
            
        Returns:
            True if sent successfully, False otherwise
        """
        html_content = f"""
        <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>שלום {user_name},</h2>
            <p>ברוכים הבאים ל-Tik-Tax! 🎉</p>
            <p>אנחנו שמחים שהצטרפת אלינו. עכשיו תוכל לנהל את כל הקבלות שלך בקלות ובמהירות.</p>
            <h3>מה אפשר לעשות עכשיו?</h3>
            <ul style="line-height: 1.8;">
                <li>📸 העלה קבלות בקלות עם המצלמה</li>
                <li>🤖 קבל זיהוי אוטומטי של הפרטים</li>
                <li>📁 שמור בארכיון מאובטח ל-7 שנים</li>
                <li>📊 ייצא לאקסל בקליק אחד</li>
            </ul>
            <p style="text-align: center; margin: 30px 0;">
                <a href="{settings.FRONTEND_URL}/dashboard" 
                   style="background-color: #2563EB; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 6px; display: inline-block;">
                    התחל עכשיו
                </a>
            </p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #E5E7EB;">
            <p style="color: #9CA3AF; font-size: 12px;">
                צריך עזרה? פנה אלינו בכל זמן.<br>
                בברכה,<br>צוות Tik-Tax
            </p>
        </div>
        """
        
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject='ברוכים הבאים ל-Tik-Tax! 🎉',
            html_content=html_content
        )
        
        try:
            response = self.client.send(message)
            logger.info(f"Welcome email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send welcome email to {to_email}: {str(e)}")
            return False
    
    async def send_subscription_reminder(self, to_email: str, user_name: str, days_remaining: int) -> bool:
        """
        Send subscription expiration reminder
        
        Args:
            to_email: Recipient email
            user_name: User's full name
            days_remaining: Days until subscription expires
            
        Returns:
            True if sent successfully, False otherwise
        """
        html_content = f"""
        <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>שלום {user_name},</h2>
            <p>המנוי שלך ב-Tik-Tax יפוג בעוד {days_remaining} ימים.</p>
            <p>כדי להמשיך ליהנות מכל היתרונות, חדש את המנוי שלך עכשיו.</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="{settings.FRONTEND_URL}/profile?tab=subscription" 
                   style="background-color: #2563EB; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 6px; display: inline-block;">
                    חדש מנוי
                </a>
            </p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #E5E7EB;">
            <p style="color: #9CA3AF; font-size: 12px;">
                בברכה,<br>צוות Tik-Tax
            </p>
        </div>
        """
        
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=f'המנוי שלך יפוג בעוד {days_remaining} ימים - Tik-Tax',
            html_content=html_content
        )
        
        try:
            response = self.client.send(message)
            logger.info(f"Subscription reminder sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send subscription reminder to {to_email}: {str(e)}")
            return False


# Singleton instance
email_service = EmailService()

