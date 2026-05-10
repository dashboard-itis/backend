from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    group_id: int | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
    expires_in: int
    scope: str


class LogoutResponse(BaseModel):
    success: bool


class RegisterResponse(BaseModel):
    success: bool


class ConfirmAccountRequest(BaseModel):
    user_id: int
    code: str = Field(min_length=1, max_length=100)


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirmRequest(BaseModel):
    user_id: int
    code: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8)
    password_confirm: str = Field(min_length=8)


class MessageResponse(BaseModel):
    success: bool
    message: str
