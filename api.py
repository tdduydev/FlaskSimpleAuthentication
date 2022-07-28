import secrets
from flask import current_app, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from flask_simple_auth.simple_auth import SimpleAuth
from datetime import datetime

auth_blueprint = Blueprint("simple_auth", __name__, url_prefix="/auth")

@auth_blueprint.route("/login", methods=["POST"])
def login():
    simple_auth:SimpleAuth = current_app.extensions.get("simple_auth")
    db:SQLAlchemy = current_app.extensions.get("sqlalchemy")
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        return {"msg": "Thiếu tên đăng nhập"},400

    if not password:
        return {"msg": "Thiếu mật khẩu"},400

    # VALIDATE tai_khoan
    tai_khoan = simple_auth.default_account_model.query.filter_by(username=username).first()
    if tai_khoan is None:
        return  {"msg": "Tài khoản không tồn tại"},400
    password = tai_khoan.salt + password
    if not simple_auth._password_verification_callback(password, tai_khoan.password):
        return {"msg":"Mật khẩu không chính xác"},400
    
    tai_khoan_data = simple_auth.default_account_schema().dump(tai_khoan)
    token = simple_auth.save_token(tai_khoan_data)

    res = simple_auth.return_login_content(tai_khoan_data, token)
    return res,200

@auth_blueprint.route("/register", methods=["POST"])
def register():
    simple_auth:SimpleAuth = current_app.extensions.get("simple_auth")
    db = current_app.extensions.get("sqlalchemy").db
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 400
    
    data = request.json

    if not data.get("username", None):
        return {"msg": "Thiếu tên đăng nhập"},400

    if not data.get("password", None):
        return {"msg": "Thiếu mật khẩu"},400

    # VALIDATE tai_khoan
    tai_khoan = simple_auth.default_account_model.query.filter_by(username=data.get("username")).first()
    if tai_khoan:
        return  {"msg": "Tài khoản đã tồn tại"},400
    data["salt"] = secrets.token_hex(8)
    data["password"] = simple_auth.encrypt_password(data["salt"]+data["password"])
    created_tai_khoan = simple_auth.default_account_schema().load(data)
    db.session.add(created_tai_khoan)
    db.session.commit()

    return {"msg":"Đăng ký tài khoản thành công"},200