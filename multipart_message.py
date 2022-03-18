from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.message import Message

import typing


class MultipartMessage():
    """
    An easy way to create multipart email for use with python's smtplib.
    Built on top of the email module.

    The 'message' attribute is a MIMEMultipart object. This is the actual email message.
    Use the 'message' attribute directly in smtplib.SMTP.send_message to send the email.
    Use the 'message' attribute directly to have more control over the email.

    For the lazy people, by the a lazy person.
    """
    def __init__(self, subject: str, sender: str, recipients: typing.Union[str, list[str]] = None):
        self.subject = subject
        self.sender = sender
        
        if(isinstance(recipients, list)):
            recipients = ", ".join(recipients)
        
        self.recipients = recipients

        self.message = MIMEMultipart()
        self.message["Subject"] = subject
        self.message["From"] = sender
        self.message["To"] = recipients

    
    def attach(self, payload: Message) -> None:
        """
            Attach any type of email.message.Message object.
            A direct wrapper around email.mime.multipart.MIMEMultipart(...).attach.
        """
        self.message.attach(payload)

    
    def attach_text(self, payload: str, mime_type: str = "plain") -> None:
        """
        Attach a string as a MIMEText object with the given mime_type to the email.
        The given string is attached as a part of the main email body.
        mime_type can be "plain" or "html" (or may be something else too, as long as it is somekind of text).

        A thin wrapper around email.mime.multipart.MIMEMultipart(...).attach.
        """
        self.message.attach(MIMEText(payload, mime_type))
    
    
    def attach_text_file(self, filename: str, mime_type: str = "plain", data: dict = None, as_file = True) -> None:
        """
        Attach a text file as a MIMEText object with the given mime_type to the email.
        Attach the file as a attachment if as_file is True.
        Otherwise attach the file as a part of the main email body.

        The given file can be of any type of text file. (e.g. .txt, .md, .html, .csv etc.)

        A wrapper around email.mime.multipart.MIMEMultipart(...).attach.
        """
        with open(filename, "r") as f:
            body: str = f.read()

        if(data):
            body = body.format(**data)

        payload = MIMEText(body, mime_type)
        
        if(as_file):
            payload['Content-Disposition'] = 'attachment; filename="%s"' % filename
    
        self.message.attach(payload)
    
    
    def attach_file(self, filename: str) -> None:
        """
        Attach a file as a MIMEApplication object to the email.
        """
        with open(filename, "rb") as f:
            payload = MIMEApplication(f.read(), Name=filename)
            payload['Content-Disposition'] = 'attachment; filename="%s"' % filename
            self.message.attach(payload)

