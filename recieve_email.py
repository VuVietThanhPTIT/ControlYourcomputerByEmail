import imaplib
import email
from email.header import decode_header, make_header
from config import *


def decode_mime(value):
	if not value:
		return ""
	return str(make_header(decode_header(value)))
# decode header and then combine them and turn into str 


class ReceiveEmail:
	def __init__(self, sender_email=email_sender, app_key=key):
		self.sender_email = sender_email
		self.app_key = app_key

	def read_latest_body(self):
		mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
		mail.login(self.sender_email, self.app_key)
		mail.select("inbox")

		status, data = mail.search(None, "ALL")

		ids = data[0].split()
      # data trả về list id email cần split 

		if not ids:
			mail.logout()
			return "", ""

		latest_id = ids[-1]
     # lấy email mới nhất
		status, msg_data = mail.fetch(latest_id, "(RFC822)")
		raw = msg_data[0][1]
     # toàn bộ dưới dạng byte 

		msg = email.message_from_bytes(raw)

		sender = decode_mime(msg.get("From"))
		subject = decode_mime(msg.get("Subject"))

		mail.logout()
		print(subject)
		return sender, subject