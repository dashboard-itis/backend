from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.session import SessionDep
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserPublic
from app.schemas.token import Token
from app.utils.security import verify_password, create_access_token
from datetime import timedelta
from app.core.settings import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserPublic)
async def register(user_data: UserCreate, db: SessionDep):
    service = UserService(db)

    existing = await service.get_by_email(user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    user = await service.create(user_data)
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: SessionDep = None
):
    service = UserService(db)

    user = await service.get_by_email(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    db_user = await service.repo.get(user.id)

    if not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

    token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )

    return Token(access_token=token, token_type="bearer")