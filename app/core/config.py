from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# ==========================
# JWT Configuration
# ==========================

SECRET_KEY = "greencode_analyzer_super_secret_key_2026"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

ACCESS_TOKEN_EXPIRE = timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
)

# ==========================
# Google OAuth Configuration
# ==========================

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

# ==========================
# Email Configuration
# ==========================

MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_STARTTLS = os.getenv("MAIL_STARTTLS", "True") == "True"
MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS", "False") == "True"