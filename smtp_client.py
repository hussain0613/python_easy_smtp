import smtplib
import typing
from typing import Sequence


class SMTPClient():
    """
    An easy way to send an email using smtp.
    Built on top of the smtplib module.
    
    For the lazy people, by the a lazy person.
    """
    def __init__(self, config: dict):
        self.host = config.get("MAIL_SERVER", "localhost")
        self.port = config.get("MAIL_PORT", 465)
        self.username = config.get("MAIL_USERNAME", None)
        self.password = config.get("MAIL_PASSWORD", None)

        if(config.get("MAIL_USE_TLS", '0') == '0'): 
            self.use_tls = False
        else: 
            self.use_tls = True

    def send_message(self, msgobj, from_addr: str = None, to_addrs: typing.Union(str, Sequence[str]) = None) -> None:
        """
        Send the email message.
        A wrapper around smtplib.SMTP(...).send_message.
        """
        with smtplib.SMTP(self.host, self.port) as server:
            if(self.use_tls):
                server.starttls()
            if(self.username and self.password):
                server.login(self.username, self.password)
            server.send_message(msgobj, from_addr=from_addr, to_addrs=to_addrs)

