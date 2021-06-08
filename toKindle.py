#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import base64
import codecs

gmail_user = 'userstar.jl@gmail.com'
gmail_password = 'j10551055' # your gmail password
msg = MIMEMultipart('mixed')
#msg = MIMEText('发送邮件php utf 8 乱码phpmailer_网络_坚持是世界上每个有所')
msg['Subject'] = 'Test中文'
msg['From'] = gmail_user
msg['To'] = 'userstar.jl@gmail.com'

attachment = MIMEBase('application', 'octet-stream')
test_str = "encoders.encode_base64(attachment)"
test_str = u"金剛經 encoders"
#res = ''.join(format(ord(i), 'b') for i in test_str) 
#res = base64.b64encode(test_str.encode("utf-8"))
#attachment.set_payload(test_str.decode('gbk'))
#attachment.set_payload(str(test_str.encode('utf-8').decode('utf-8')))

attachment.set_payload(open("f1.txt", 'rb').read())
encoders.encode_base64(attachment)
attachment.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', "測試中文檔名.txt") )

'''
attachment = MIMEText('发送邮件php utf 8 乱码phpmailer_网络_坚持是世界上每个有所', 'plain', 'utf-8')
encoders.encode_base64(attachment)
attachment.add_header('Content-Disposition', 'attachment; filename="abc.txt"')
'''
msg.attach(attachment)
'''
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>坚持是世界上每个有所...<br>
       Here is the <a href="https://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""
part2 = MIMEText(html, 'html', 'utf-8')
#Header(basename, 'utf-8').encode()
part2.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', "中文.htm") )
#part2.add_header('Content-Disposition', 'attachment', filename="abc.html")
encoders.encode_base64(part2)
part2.add_header('Content-ID','<1>')
part2.add_header('X-Attachment-Id','1')
msg.attach(part2)
'''
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)
server.send_message(msg)
server.quit()

print ("Content-type:text/html\n")
print('Email sent!')