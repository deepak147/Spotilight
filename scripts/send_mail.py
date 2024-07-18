import os
import smtplib
import ssl
from tabulate import tabulate

from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(top_5_songs_min, total_time_listened_hrs, top_songs_art_played, top_art_played):
    
    today = datetime.today().date()
    one_day_ago = today - timedelta(days=1)
    
    port = 465
    password = "aokeluotzlvfsttp"
    sender_email = os.environ["GMAIL_USER"]
    receiver_email = os.environ.get("GMAIL_USER")

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Spotify - Daily Roundup {today}"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""\
    Here are your stats for your daily round up for Spotify. 
    Dates included: {one_day_ago} - {today}:
    
    Total Time Listened: {total_time_listened_hrs} hours.
    You listened to these songs and artists a lot here are your top 5!
    {top_songs_art_played}
    You spent the most time listening to these songs:
    {top_5_songs_min}
    You spend the most time listening to these artists:
    {top_art_played}
    """
    html = f"""\
    <html>
        <body>
            <h4>
            Here are your stats for your daily round up for Spotify.
            </h4>
            <p>
            Dates included: {one_day_ago} - {today}
            <br>
            Total Time Listened: {total_time_listened_hrs} hours.
            <br>
            <h4>
            You listened to these songs and artists a lot here are your top 5!
            </h4>
            {tabulate(top_songs_art_played, tablefmt='html')}
            <h4>
            You spend a lot of time listening to these songs!
            </h4>
            {tabulate(top_5_songs_min, tablefmt='html')}
            <h4>
            You spend a lot of time listening to these artists!
            </h4>
            {tabulate(top_art_played, tablefmt='html')}
            </p>
        </body>
    </html>"""

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())