from enum import StrEnum, auto


class Role(StrEnum):
    superuser = auto()
    admin = auto()
    service = auto()
    moderator = auto()
    user = auto()

    @property
    def description(self) -> str:
        return {
            self.superuser.value: "Superuser role. Has all permissions.",
            self.admin: "Admin role. Can manage users and services.",
            self.service.value: "Service role. Can manage services.",
            self.moderator.value: "Moderator role. Can moderate content.",
            self.user.value: "User role. Can access the service.",
        }[self.value]


class RequestTokenType(StrEnum):
    reset_password = auto()
    verify_email = auto()
