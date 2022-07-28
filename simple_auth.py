import functools
from flask import Flask
from flask import request, Blueprint
import typing as t


class SimpleAuth(object):
    app = None
    db = None
    default_account_model = None
    default_account_schema = None
    enable_simple_auth=False
    
    _password_encryption_callback = None
    _password_verification_callback = None
    _login_save_token_callback = None
    _login_return_callback =None
    
    def __init__(self, app=None, use_simple_auth=False):
        self.enable_simple_auth = use_simple_auth
        if app:
            self.init_app(app)

            
    def init_app(self, app, account_model,account_schema):
        from flask_simple_auth.default_callback import (
            _default_password_encryption_callback,
            _default_password_verification_callback,
            _default_login_save_token_callback,
            _default_login_return_callback
        )
        self.default_account_model = account_model
        self.default_account_schema = account_schema
        if not app or not isinstance(app, Flask):
            raise TypeError("Invalid Flask app instance.")
        self.app = app

        self.db = app.extensions.get("sqlalchemy",None)
        if not self.db:
            raise ValueError("SQLalchemy database is missing before initialization. Please initialize SQLalchemy before this extensions")
        if not app.extensions.get("redis",None):
            raise ValueError("Redis cache is missing before initialization. Please initialize Redis before this extensions")
        app.extensions["simple_auth"] = self
        self._password_encryption_callback = _default_password_encryption_callback
        self._password_verification_callback =_default_password_verification_callback
        self._login_save_token_callback = _default_login_save_token_callback
        self._login_return_callback = _default_login_return_callback
        
        if self.enable_simple_auth:
            from flask_simple_auth.api import auth_blueprint
            app.register_blueprint(auth_blueprint)
            


            
    def encrypt_password(self,password):
        return self._password_encryption_callback(password)
    
    def verify_password(self,input,hash):
        return self._password_verification_callback(input,hash)
    
    def save_token(self, data:dict):
        return self._login_save_token_callback(data)
    
    def return_login_content(self,account_data:dict,token:str):
        return self._login_return_callback(account_data,token)
    
    def _password_encryption_loader(self, callback):
        self._password_encryption_callback = callback
        return callback
    
    def _password_verification_loader(self, callback):
        self._password_verification_callback = callback
        return callback
    
    def _login_save_token_loader(self, callback):
        self._login_save_token_callback = callback
        return callback
    
    def _login_return_loader(self, callback:t.Callable[[dict],t.Tuple[dict,int]]):
        self._login_return_callback = callback
        return callback
    
    def _change_password_encryption(self):
        def wrapper(fn):
            @functools.wraps(fn)
            def decorator(*args, **kwargs):
                self._password_encryption_loader(fn)
                return fn(*args, **kwargs)
            return decorator
        return wrapper
    
    def _change_password_verification_process(self):
        def wrapper(fn):
            @functools.wraps(fn)
            def decorator(*args, **kwargs):
                self._password_verification_loader(fn)
                return fn(*args, **kwargs)
            return decorator
        return wrapper
    
    def _change_login_save_token(self):
        def wrapper(fn):
            @functools.wraps(fn)
            def decorator(*args, **kwargs):
                self._login_save_token_loader(fn)
                return fn(*args, **kwargs)
            return decorator
        return wrapper
    
    def _change_login_return(self):
        def wrapper(fn):
            @functools.wraps(fn)
            def decorator(*args, **kwargs):
                self._login_return_loader(fn)
                return fn(*args, **kwargs)
            return decorator
        return wrapper