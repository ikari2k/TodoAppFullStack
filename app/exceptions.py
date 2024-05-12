class NotFoundException(Exception):
    "Raised when db item is not found in DB"
    pass


class PasswordChangeError(Exception):
    "Raised when password user was unable to verify his old password on password change"
    pass
