# ✉️ Internship Email Sender Tool

📬 Automatically send personalized internship application emails to multiple companies using CSV data and language-based templates.

---

## 🚀 Features

- 🇬🇧🇫🇷 **Language Support**: Sends emails in English or French based on CSV column
- 📎 **Auto-Attach**: Includes your CV and signature automatically
- 🐛 **Debug Mode**: Prints detailed logs to the console for easier debugging

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Folders and Templates

```bash
mkdir templates
# Add your email templates:
# - templates/email_en.txt
# - templates/email_fr.txt
```
**Note**: You can include in the template dynamic variables which are `{{RESPONSIBLE_NAME}}` and `{{COMPANY_NAME}}` which will be then replaced with the real values when loading the template.

### 3. Configure Environment Variables

Create a `.env` file in the root directory with the following:

```env
# Email Configuration
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password

# File Paths
SIGNATURE_PATH=signature.jpg
CV_EN_PATH=cv_en.pdf
CV_FR_PATH=cv_fr.pdf
INTERNSHIPS_FILE=internships.csv

# Settings
DEBUG_MODE=true
```

---

## 📊 CSV Format

Your `internships.csv` should follow this structure:

| company_name | country | responsible_name | email            | language |
| ------------ | ------- | ---------------- | ---------------- | -------- |
| Google       | USA     | John Doe         | john@example.com | en       |
| Dassault     | France  | Marie Dupont     | marie@example.fr | fr       |

---

## 📤 Usage

Run the script with:

```bash
python3 main.py
```

The script will:

1. Read your CSV and templates
2. Personalize and prepare emails
3. Let you preview before sending (if DEBUG_MODE is `true`)

---

## 🧠 Notes

- Use a Gmail [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password
- Set `language` in CSV to `en` or `fr` to select the email template
- Signature image should be a horizontal PNG or JPG, ideally **300–600px wide** and **70–150px tall**

---

## 🗂 Project Structure

```
internship-email-sender/
├── main.py                 # Main script
├── utils.py                # Email and validation helpers
├── .env                    # Environment config
├── requirements.txt        # Dependencies
├── internships.csv         # Company data
└── templates/
    ├── email_en.txt
    └── email_fr.txt
```
