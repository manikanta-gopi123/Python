import mysql.connector
import requests
import zipfile
import os
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import pytz

# ---------------------------
# DATABASE CONFIGURATION
# ---------------------------
db_config = {
    "host": "20.233.62.109",
    "user": "wasupport",
    "password": "35g1waUV95R6",
    "database": "whatsapp",
    "port": 4566
}

# ---------------------------
# FILE SETTINGS
# ---------------------------
temp_folder = "downloaded_audio"
headers = {"User-Agent": "Mozilla/5.0"}

# ---------------------------
# EMAIL SETTINGS (SMTP)
# ---------------------------
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USER = "nadikatla.gopi@vectramind.com"
SMTP_PASS = "gfxbwjprrsmbhnny"

TO_EMAIL = [
    "Rajini.balasuriya@feedbackme.com",
    "rajesh.nair@feedbackme.com"
]
CC_EMAIL = [
    "wa.support@vectramind.com"
]

# ---------------------------
# FETCH DATA
# ---------------------------
def fetch_records(start_str, end_str):
    print(f"Fetching records from {start_str} to {end_str}")
    query = f"""
    SELECT DISTINCT mobile_no,
    JSON_UNQUOTE(JSON_EXTRACT(CONVERT(user_data USING utf8), '$.surveyid')) AS surveyid,
    MAX(CONCAT(
        'https://wa.me.synapselive.com/images/',
        JSON_UNQUOTE(JSON_EXTRACT(COALESCE(NULLIF(CONVERT(m.msg_content USING utf8mb4), ''),'{{}}'),'$.id')),
        '.ogg'
    )) AS audiourl
    FROM wa_user_chat_cdr c
    LEFT JOIN wa_message_cdr cdr ON UUID=c.trans_id
    LEFT JOIN wa_mo_message m ON m.from_number = mobile_num AND c.msg_id=m.msg_id
    WHERE cdr.customer_id = 38
      AND template_name LIKE '%feedback%'
      AND cdr.module_type = 'http'
      AND cdr.received_time BETWEEN '{start_str}' AND '{end_str}'
      AND m.msg_type = 'audio'
    GROUP BY surveyid, mobile_no
    HAVING audiourl IS NOT NULL
    """

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    print(f"Total records fetched: {len(records)}")
    return records

# ---------------------------
# DOWNLOAD + ZIP
# ---------------------------
def download_and_zip(records, start_str, end_str):
    os.makedirs(temp_folder, exist_ok=True)

    downloaded_files = []
    seen_urls = set()

    for rec in records:
        url = rec.get("audiourl")
        mobile = rec.get("mobile_no")
        sid = rec.get("surveyid")

        if not url or url in seen_urls:
            continue

        file_name = f"{mobile}_{sid}.ogg"
        file_path = os.path.join(temp_folder, file_name)

        try:
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()

            with open(file_path, "wb") as f:
                f.write(r.content)

            downloaded_files.append(file_path)
            seen_urls.add(url)
            print(f"Downloaded: {file_name}")

        except Exception as e:
            print(f"Failed to download {url}: {e}")

    if not downloaded_files:
        return None

    zip_name = f"Audio_Files_{start_str[:10]}_to_{end_str[:10]}.zip"

    with zipfile.ZipFile(zip_name, "w") as zipf:
        for f in downloaded_files:
            zipf.write(f, os.path.basename(f))
            os.remove(f)

    os.rmdir(temp_folder)
    print(f"ZIP created: {zip_name}")

    return os.path.abspath(zip_name)

# ---------------------------
# SEND MAIN EMAIL (WITH ZIP)
# ---------------------------
def send_email_smtp(attachment_path, start_str, end_str):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(TO_EMAIL)
    msg["Cc"] = ", ".join(CC_EMAIL)
    msg["Subject"] = f"Audio Files - {start_str[:10]} to {end_str[:10]}"

    msg.set_content(
        f"""Hi Team,

Please find the attached audio files for the period from
{start_str} to {end_str}.

Regards,
Gopi"""
    )

    if attachment_path:
        with open(attachment_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="zip",
                filename=os.path.basename(attachment_path)
            )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    print("Main email sent successfully")

# ---------------------------
# SEND NOT-SCHEDULED EMAIL
# ---------------------------
def send_not_scheduled_email(today):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = ["nadikatla.gopi@vectramind.com"]
    msg["Subject"] = "Scheduled Job Skipped"

    msg.set_content(
        f"""Hi Team,

Today ({today.strftime('%A, %d-%b-%Y')}) is not a scheduled day.

This job runs only on:
- Monday
- Friday

No data processing was performed today.

Regards,
Gopi
"""
    )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    print("Not-scheduled notification email sent")

# ---------------------------
# MAIN JOB
# ---------------------------
def job():
    ist = pytz.timezone("Asia/Kolkata")
    today = datetime.now(ist)
    weekday = today.weekday()  # Monday=0, Friday=3

    if weekday == 0:  # Monday
        start_date = today - timedelta(days=3)  # Friday
        end_date = today - timedelta(days=1)    # Sunday

    elif weekday == 4:  # Friday
        start_date = today - timedelta(days=4)  # Monday
        end_date = today - timedelta(days=1)    # Thursday

    else:
        send_not_scheduled_email(today)
        return

    start_str = start_date.strftime('%Y-%m-%d 00:00:00')
    end_str = end_date.strftime('%Y-%m-%d 23:59:59')

    records = fetch_records(start_str, end_str)

    if records:
        zip_path = download_and_zip(records, start_str, end_str)
        if zip_path:
            send_email_smtp(zip_path, start_str, end_str)
    else:
        print("No records found")

# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    job()
