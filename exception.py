class AuthenticationException(Exception):
    def __init__(self, message="Authentication failed, pelase check your username or password"):
        super().__init__(message)
        