import bcrypt


class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        plain_password_bytes = plain_password.encode("utf-8")
        hashed_password_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
