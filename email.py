from email.message import EmailMessage
import smtplib
import ssl



def enrollmentEmail(reciEmail):
    
    receiverEmail = reciEmail

    senderEmail = 'accutime032@gmail.com'
    passWord = 'Ambi1976'
    emailSubject = "Enrollment Successful"
    body = "Thank you for enrolling using the Acutime enrolment system"
    
    emailMess = EmailMessage()
    emailMess["From"] = senderEmail
    emailMess["To"] = receiverEmail
    emailMess["Subject"] = emailSubject
    emailMess.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(senderEmail, passWord)
        server.sendmail(senderEmail,receiverEmail,emailMess.as_string())

enrollmentEmail("rishia2707@gmail.com")