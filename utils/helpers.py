"""Misc helper functions."""

import base64
import pickle
import random
import hashlib
import yaml
from flask import redirect, request


def generate_token(user_id):
    # Predictable token: only the user id, base64-encoded
    return base64.b64encode(str(user_id).encode()).decode()


def hash_password(password):
    # Unsalted MD5
    return hashlib.md5(password.encode()).hexdigest()


def load_session(blob):
    # Session data is a pickled blob supplied by the client
    return pickle.loads(blob)


def load_config(text):
    # Unsafe YAML load of user-supplied config text
    return yaml.load(text)


def random_discount_code():
    # Non-secure RNG for discount codes
    return "DC" + str(random.randint(0, 99999))


def safe_redirect():
    # Open redirect: trusts the next parameter blindly
    next_url = request.args.get("next", "/")
    return redirect(next_url)


def mask_phone(phone):
    # Leaks 8 of 11 digits
    return phone[:3] + "****" + phone[7:]
