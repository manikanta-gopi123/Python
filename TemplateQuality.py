import mysql.connector
import smtplib
from email.message import EmailMessage
import os
from datetime import datetime

# ---------------------------
# CONSTANT FILE (TRACK STATUS)
# ---------------------------
STATUS_FILE = "daily_status.txt"

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
# EMAIL SETTINGS
# ---------------------------
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USER = "nadikatla.gopi@vectramind.com"
SMTP_PASS = "gfxbwjprrsmbhnny"

TO_EMAIL = ["nadikatla.gopi@vectramind.com"]


# ---------------------------
# FETCH DATA
# ---------------------------
def fetch_records():
    query = """
    SELECT cus.customer_name, tem.template_name, tem.status, tem.quality_score
    FROM um_customer cus
    INNER JOIN wa_template tem ON tem.customer_id = cus.id
    WHERE tem.quality_score IN ('YELLOW','RED')
      AND tem.quality_score_date >= (NOW() - INTERVAL 10 MINUTE)
    ORDER BY cus.customer_name DESC
    """

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute(query)
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records


# ---------------------------
# SEND EMAIL
# ---------------------------
def send_email(subject, body):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(TO_EMAIL)
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    print(f"Email sent: {subject}")


# ---------------------------
# MAIN ALERT LOGIC
# ---------------------------
def process_run():
    records = fetch_records()

    # ✅ If records found → send alert
    if records:
        body = "Hi Gopi,\n\nTemplate quality dropped:\n\n"

        for r in records:
            body += f"{r['customer_name']} | {r['template_name']} | {r['status']} | {r['quality_score']}\n"

        body += "\nRegards,\nGopi"

        send_email("🚨 Template Quality Alert", body)

        # Mark that issues occurred today
        with open(STATUS_FILE, "w") as f:
            f.write("ISSUES_FOUND")

    else:
        print("No records found, no email sent.")


# ---------------------------
# END OF DAY SUMMARY
# ---------------------------
def end_of_day_summary():
    today = datetime.now().strftime("%Y-%m-%d")

    # If file doesn't exist OR no issues recorded
    if not os.path.exists(STATUS_FILE):
        send_email(
            "✅ Daily Summary - No Issues",
            f"Hi Gopi,\n\nNo YELLOW/RED template issues found on {today}.\n\nRegards,\nGopi"
        )
    else:
        print("Issues were found today — no summary email needed.")

    # Reset file for next day
    if os.path.exists(STATUS_FILE):
        os.remove(STATUS_FILE)


# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    process_run()

    # 👉 Run this separately at end of day (via scheduler)
    # end_of_day_summary()