"""Email sending utilities for Mise."""

import base64
import logging
import os
from typing import Optional

log = logging.getLogger(__name__)


def send_deliverables_email(
    to_email: str,
    subject: str,
    body: str,
    attachment_data: bytes,
    attachment_filename: str,
    from_email: str = "hello@getmise.io"
) -> bool:
    """
    Send deliverables email with attachment using SendGrid.

    Args:
        to_email: Recipient email address
        subject: Email subject line
        body: Email body (plain text)
        attachment_data: Binary data of the attachment
        attachment_filename: Name of the attachment file
        from_email: Sender email address

    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

        # Get SendGrid API key from environment
        api_key = os.environ.get("SENDGRID_API_KEY")
        if not api_key:
            log.warning("SENDGRID_API_KEY not configured - email will not be sent")
            return False

        # Create message
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=body
        )

        # Add attachment
        encoded_file = base64.b64encode(attachment_data).decode()
        attached_file = Attachment(
            FileContent(encoded_file),
            FileName(attachment_filename),
            FileType('application/zip'),
            Disposition('attachment')
        )
        message.attachment = attached_file

        # Send email
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        log.info(f"Email sent successfully to {to_email}. Status code: {response.status_code}")
        return True

    except Exception as e:
        log.error(f"Failed to send email to {to_email}: {e}")
        return False


def format_payroll_email_subject(start_date, end_date) -> str:
    """Format email subject for payroll tip reports."""
    return f"Mise Docs: Tip Reports ({start_date.strftime('%-m/%-d/%y')} - {end_date.strftime('%-m/%-d/%y')})"


def format_payroll_email_body(restaurant_name: str, start_date, end_date) -> str:
    """Format email body for payroll tip reports."""
    return f"""Hello,

Your Mise Docs are ready for the week of {start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}.

Attached is a zip file containing:
- Tip Report PDF (weekly totals and shift breakdown)
- Excel spreadsheet (Weekly Totals and Shift Breakdown sheets)
- Toast-ready PayrollExport CSV

Thank you for using Mise!

---
{restaurant_name}
Sent from Mise (getmise.io)
"""
