from datetime import datetime, timedelta
import random

# Stores pending registrations temporarily
pending_registrations = {}


def generate_otp():
    return str(random.randint(100000, 999999))


def save_registration(identifier: str, user_data: dict):

    otp = generate_otp()

    pending_registrations[identifier] = {
        "user_data": user_data,
        "otp": otp,
        "expires": datetime.now() + timedelta(minutes=5)
    }

    return otp


def verify_otp(identifier: str, entered_otp: str):

    record = pending_registrations.get(identifier)

    if not record:
        return False

    if datetime.now() > record["expires"]:
        pending_registrations.pop(identifier)
        return False

    if record["otp"] != entered_otp:
        return False

    return True


def get_pending_user(identifier: str):

    record = pending_registrations.get(identifier)

    if not record:
        return None

    return record["user_data"]


def delete_pending_user(identifier: str):

    pending_registrations.pop(identifier, None)


def resend_otp(identifier: str):

    record = pending_registrations.get(identifier)

    if not record:
        return None

    otp = generate_otp()

    record["otp"] = otp
    record["expires"] = datetime.now() + timedelta(minutes=5)

    return otp