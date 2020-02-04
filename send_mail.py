import smtplib
from email.mime.text import MIMEText

def send_mail(customer, dealer, rating, comments, useremail):
    port=2525
    smtp_server='smtp.mailtrap.io'
    login='8203fc5b11e6a6'
    password='4dcc8f1d09f4ee'
    message= f"<h3>New feedback submitted</h3><ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li><li>User Email: {useremail}</li></ul>"

    sender_email="email1@example.com"
    receiver_email="email2@example.com"
    msg=MIMEText(message, 'html')
    msg['Subject'] = 'Hyundai Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    #send email
    with smtplib.SMTP(smtp_server,port) as server:
        server.login(login,password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
