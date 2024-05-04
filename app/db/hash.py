import bcrypt


class Hash:
    @staticmethod
    def bcrypt(password: str) -> bytes:
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password

    @staticmethod
    def verify(plain_password: str, hashed_password: bytes):
        plain_password_bytes = plain_password.encode("utf-8")
        return bcrypt.checkpw(plain_password_bytes, hashed_password)
