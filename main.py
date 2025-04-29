import smtplib
import os
import pandas as pd
from dotenv import load_dotenv
from utils import generate_email_body, create_email

# ✅ Load environment variables from .env
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
YOUR_NAME = os.getenv("YOUR_NAME")
CSV_PATH = os.getenv("CSV_PATH", "companies.csv")
CV_EN_PATH = os.getenv("CV_EN_PATH", "assets/CV_en.pdf")
CV_FR_PATH = os.getenv("CV_FR_PATH", "assets/CV_fr.pdf")
SIGNATURE_PATH = os.getenv("SIGNATURE_PATH", "assets/signature.png")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# ✅ Load company list
df = pd.read_csv(CSV_PATH)
print(f"📊 Loaded {len(df)} companies from {CSV_PATH}")

# ✅ Prepare and send emails
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL, PASSWORD)

    for _, row in df.iterrows():
        email = row["email"]
        company = row["company_name"]
        country = row["country"]
        language = row.get("language", "en")
        responsible = row.get("responsible_name", None)

        lang, body = generate_email_body(company, country, language, responsible_name=responsible, is_debug=DEBUG)
        if not body:
            continue

        msg = create_email(
            recipient_email=email,
            body=body,
            language=lang,
            sender_name=YOUR_NAME,
            sender_email=EMAIL,
            signature_path=SIGNATURE_PATH,
            cv_en_path=CV_EN_PATH,
            cv_fr_path=CV_FR_PATH,
            is_debug=DEBUG
        )

        try:
            server.sendmail(EMAIL, email, msg.as_string())
            print(f"✅ Sent to {email}")
        except Exception as e:
            print(f"❌ Failed to send to {email}: {e}")
