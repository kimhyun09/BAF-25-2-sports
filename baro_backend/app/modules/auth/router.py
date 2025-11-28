from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

from app.modules.auth.schemas import (
    LoginRequestDto,
    LoginResponseDto,
    SignUpRequestDto,
    ProfileUpdateRequestDto,
    AuthUser,
)
from app.modules.auth.service import (
    login_with_kakao,
    create_jwt_token,
    verify_jwt_token,
    sign_up,
    update_profile,
    get_user,
    delete_user,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

# JWT 토큰 추출용 (Swagger UI 인증 버튼 활성화)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/kakao-login")

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        user_id = verify_jwt_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return user_id

@router.post("/kakao-login", response_model=LoginResponseDto)
def kakao_login_endpoint(req: LoginRequestDto):
    try:
        # Pydantic alias 덕분에 req.kakao_access_token으로 접근 가능
        user = login_with_kakao(req.kakao_access_token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    jwt_token = create_jwt_token(user.id)
    return LoginResponseDto(access_token=jwt_token, user=user)

@router.post("/sign-up", response_model=AuthUser)
def sign_up_endpoint(
    req: SignUpRequestDto,
    user_id: UUID = Depends(get_current_user_id),
):
    return sign_up(user_id, req)

@router.get("/me", response_model=AuthUser)
def get_my_profile(user_id: UUID = Depends(get_current_user_id)):
    try:
        return get_user(user_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="User not found")

@router.patch("/me/profile", response_model=AuthUser)
def update_my_profile(
    req: ProfileUpdateRequestDto,
    user_id: UUID = Depends(get_current_user_id),
):
    return update_profile(user_id, req)

@router.post("/logout")
def logout(user_id: UUID = Depends(get_current_user_id)):
    return {"detail": "logged out"}

@router.delete("/me")
def delete_account(user_id: UUID = Depends(get_current_user_id)):
    delete_user(user_id)
    return {"detail": "account deleted"}