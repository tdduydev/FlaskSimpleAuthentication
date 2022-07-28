from datetime import datetime
import json
from passlib.context import CryptContext
from flask import current_app
from flask_jwt_extended import create_access_token, decode_token
from flask_simple_auth.simple_auth import SimpleAuth
from .helper import DateTimeEncoder


def _default_login_return(account: dict, token: str):
    return {
        "msg": "Thành công",
        "results": {
            "account": account,
            "access_token": token
        }
    }


def _default_login_save_token(account: dict) -> str:
    redis = current_app.extensions.get("redis")
    token = create_access_token(account["id"])
    decoded_token = decode_token(token)
    jti = decoded_token["jti"]
    token_type = decoded_token["type"]
    expires = datetime.fromtimestamp(decoded_token["exp"])
    revoked = False

    dbRedis = {
        "jti": jti,
        "token_type": token_type,
        "expires": expires,
        "revoked": revoked,
    }

    redis.set(f"token:{jti}", json.dumps(dbRedis, cls=DateTimeEncoder))
    return jti


_default_password_encryption_callback = CryptContext(
    schemes=["pbkdf2_sha256"], deprecated="auto").hash
_default_password_verification_callback = CryptContext(
    schemes=["pbkdf2_sha256"], deprecated="auto").verify
_default_login_return_callback = _default_login_return
_default_login_save_token_callback = _default_login_save_token
