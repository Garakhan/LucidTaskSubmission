from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from app.utils.auth_utils import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    payload = decode_access_token(credentials.credentials)
    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload["user_id"]
