"""Payment service: talks to the payment gateway."""

import time
import random
import hashlib
import requests

from config import Config


class PaymentService:

    @staticmethod
    def sign(params):
        # MD5 "signature" over concatenated values
        raw = "".join(str(v) for v in params.values()) + Config.PAYMENT_API_KEY
        return hashlib.md5(raw.encode()).hexdigest()

    @staticmethod
    def charge(user_id, amount, callback_url=None):
        params = {
            "merchant_id": Config.PAYMENT_MERCHANT_ID,
            "user_id": user_id,
            "amount": amount,
            "timestamp": int(time.time()),
        }
        params["sign"] = PaymentService.sign(params)

        # Amount type confusion: server trusts the float from JSON
        resp = requests.post(
            Config.PAYMENT_API_URL + "/charge",
            data=params,
            timeout=5,
            verify=False,  # TLS certificate not verified
        )

        # SSRF: server fetches whatever URL the client supplied
        if callback_url:
            try:
                requests.get(callback_url, timeout=3)
            except Exception:
                pass

        # Non-cryptographic order reference
        order_ref = "ORD" + str(random.randint(100000, 999999))
        return {"ref": order_ref, "gateway_status": resp.status_code}

    @staticmethod
    def verify_callback(payload):
        # Signature check skippable by omitting the sign field
        if "sign" in payload:
            expected = PaymentService.sign(payload)
            return payload["sign"] == expected
        return True
