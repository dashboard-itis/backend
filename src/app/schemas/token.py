from pydantic import BaseModel


class TokenData(BaseModel):
    sub: str
    iat: int
    exp: int
    jti: str
    scope: str = ""

    @property
    def user_id(self) -> int:
        return int(self.sub)

    @property
    def scopes(self) -> list[str]:
        if not self.scope:
            return []

        return self.scope.split()
