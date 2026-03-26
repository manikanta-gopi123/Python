import mysql.connector
import requests
import zipfile
import os
import win32com.client as win32

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
# SQL QUERY
# ---------------------------
query = """
SELECT DISTINCT mobile_no,
JSON_UNQUOTE(JSON_EXTRACT(CONVERT(user_data USING utf8), '$.surveyid')) AS surveyid,
MAX(CONCAT('https://wa.me.synapselive.com/images/',
JSON_UNQUOTE(JSON_EXTRACT(COALESCE(NULLIF(CONVERT(m.msg_content USING utf8mb4), ''), '{}'),'$.id')),'.ogg')) AS audiourl
FROM wa_user_chat_cdr_bkp c
LEFT JOIN wa_message_cdr_bkp cdr ON UUID=c.trans_id
LEFT JOIN wa_mo_message_bkp m ON m.from_number = mobile_num AND c.msg_id=m.msg_id
WHERE cdr.customer_id=38
AND template_name LIKE '%feedback%'
AND cdr.module_type ='http'
AND cdr.received_time BETWEEN '2026-3-9 00:00:00' AND '2026-3-11 23:59:59'
AND m.msg_type='audio'
GROUP BY surveyid, mobile_no
HAVING audiourl IS NOT NULL

UNION ALL

SELECT DISTINCT mobile_no,
JSON_UNQUOTE(JSON_EXTRACT(CONVERT(user_data USING utf8), '$.surveyid')) AS surveyid,
MAX(CONCAT('https://wa.me.synapselive.com/images/',
JSON_UNQUOTE(JSON_EXTRACT(COALESCE(NULLIF(CONVERT(m.msg_content USING utf8mb4), ''), '{}'),'$.id')),'.ogg')) AS audiourl
FROM wa_user_chat_cdr c
LEFT JOIN wa_message_cdr cdr ON UUID=c.trans_id
LEFT JOIN wa_mo_message m ON m.from_number = mobile_num AND c.msg_id=m.msg_id
WHERE cdr.customer_id=38
AND template_name LIKE '%feedback%'
AND cdr.module_type ='http'
AND cdr.received_time BETWEEN '2026-3-9 00:00:00' AND '2026-3-11 23:59:59'
AND m.msg_type='audio'
GROUP BY surveyid, mobile_no
HAVING audiourl IS NOT NULL
"""

# ---------------------------
# OUTPUT SETTINGS
# ---------------------------
output_zip = "Audio_Files_from_9_to_11_Mar_2026.zip"
temp_folder = "downloaded_audio"

headers = {"User-Agent": "Mozilla/5.0"}

# ---------------------------
# EMAIL SETTINGS
# ---------------------------
TO_EMAIL = "nadikatla.gopi@vectramind.com"
CC_EMAIL = "prasadu.bonthu@vectramind.com.com"   # leave blank "" if not needed
SUBJECT = "Audio Files from 9 to 11 Mar 2026"
BODY = """Hi Team,

This is an automated email from CRON JOB This will run on every Monday and Tuesday and trigger email automatically from the Python code which is housted on https://github.com/manikanta-gopi123/DevOps.git.

Regards,
Gopi
"""

# ---------------------------
# FETCH DATA FROM MYSQL
# ---------------------------
def fetch_records():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute(query)
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records

# ---------------------------
# DOWNLOAD AND ZIP FILES
# ---------------------------
def download_and_zip(records, zip_name):

    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    downloaded_files = []
    seen_urls = set()

    print(f"\nTotal Records Found: {len(records)}\n")
    print("--- Starting Downloads ---\n")

    for rec in records:
        mobile = rec["mobile_no"]
        sid = rec["surveyid"]
        url = rec["audiourl"]

        if not url or url in seen_urls:
            continue

        file_ext = url.split(".")[-1]
        file_name = f"{mobile}_{sid}.{file_ext}"
        file_path = os.path.join(temp_folder, file_name)

        try:
            response = requests.get(url, headers=headers, stream=True, timeout=20)
            response.raise_for_status()

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)

            print("Downloaded:", file_name)

            downloaded_files.append(file_path)
            seen_urls.add(url)

        except Exception as e:
            print("Failed:", url, e)

    # ---------------------------
    # CREATE ZIP
    # ---------------------------
    if downloaded_files:
        print("\n--- Creating ZIP File ---\n")

        with zipfile.ZipFile(zip_name, "w") as zipf:
            for file in downloaded_files:
                zipf.write(file, os.path.basename(file))
                os.remove(file)

        print("ZIP Created Successfully →", zip_name)

        if os.path.exists(temp_folder) and not os.listdir(temp_folder):
            os.rmdir(temp_folder)

        return os.path.abspath(zip_name)

    else:
        print("No files downloaded")
        return None

# ---------------------------
# SEND EMAIL USING OUTLOOK
# ---------------------------
def send_email_outlook(attachment_path):
    try:
        outlook = win32.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)

        mail.To = "nadikatla.gopi@vectramind.com"
        mail.CC = "prasadu.bonthu@vectramind.com"
        mail.Subject = SUBJECT
        mail.Body = BODY

        if attachment_path and os.path.exists(attachment_path):
            mail.Attachments.Add(attachment_path)

        # Option 1: Send directly
        mail.Send()

        # Option 2: Open email for review before sending
        # mail.Display()

        print(f"Email sent successfully with attachment: {attachment_path}")

    except Exception as e:
        print("Failed to send email:", e)

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":

    records = fetch_records()

    if records:
        zip_path = download_and_zip(records, output_zip)

        if zip_path:
            send_email_outlook(zip_path)
    else:
        print("No records found.")