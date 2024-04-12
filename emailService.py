import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "nigeldias27@yahoo.com"
receiver_email = "nigeldias27@gmail.com"
password = ''

message = MIMEMultipart("alternative")
message["Subject"] = "Invitation to Feature Your B2B Software Product on G2"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
html = """\
<html>
  <body>
    <p>Dear [Company Name], <br><br>

I hope this email finds you well. I'm reaching out from G2, the leading platform for business software reviews and insights. We're constantly on the lookout for innovative B2B software solutions to feature on our platform, and after learning about your recent product release, we're excited to extend an invitation to showcase it on G2.<br><br>

Here at G2, we provide a comprehensive platform where businesses can discover, compare, and review software solutions tailored to their needs. With millions of monthly visitors, our platform offers unparalleled visibility and exposure for software products, helping them reach a global audience of potential customers.
<br><br>
By featuring your product on G2, you'll have the opportunity to:
<br><br>
Increase visibility: Gain exposure to our vast audience of business professionals actively seeking software solutions in your industry.<br>
Build trust: Showcase your product through unbiased user reviews and ratings, helping potential customers make informed purchasing decisions.<br>
Drive leads: Generate high-quality leads as users engage with your product listing, request demos, and explore your offering in detail.<br><br>
Adding your product to G2 is a straightforward process, and our team will be available to assist you every step of the way. We'll work with you to create a compelling product profile, gather initial reviews, and ensure that your listing accurately reflects the value proposition of your solution.
<br><br>
Moreover, featuring your product on G2 is completely free, with no upfront costs or commitments required.
<br><br>
If you're interested in taking advantage of this opportunity to showcase your B2B software product to a global audience of potential customers, <a href="http://www.g2.com">Register Now</a>.
<br><br>
Thank you for considering this invitation, and we look forward to the possibility of collaborating with you to highlight your innovative solution on G2.
<br><br>
Best Regards<br>
G2 Lead Generation Team
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects

part2 = MIMEText(html, "html")

message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465, context=context) as server:
    server.login(sender_email, password)
    print("Logged In")
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
    print("Email Sent")