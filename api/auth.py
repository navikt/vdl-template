import json
import os
from typing import List, Union

import jwt
from fastapi import Header, HTTPException
from pydantic import BaseModel


class User(BaseModel):
    name: str = None
    preferred_username: str = None
    NAVident: str = None
    groups: Union[List[str], None] = None
    azp: str = None
    azp_name: str = None


def get_authorization_token(authorization_header: str):
    if (
        not authorization_header
        or len(authorization_header.split(" ")) != 2
        or authorization_header.split(" ")[0] != "Bearer"
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid authorization scheme. Expecting Bearer token.",
        )
    return authorization_header.split(" ")[1]


def validate_token(authorization_header: str):
    url = os.environ["AZURE_APP_WELL_KNOWN_URL"]
    id_token = get_authorization_token(authorization_header)
    jwk_client = jwt.PyJWKClient(url)
    signing_key = jwk_client.get_signing_key_from_jwt(id_token)
    claims = jwt.decode(
        id_token,
        key=signing_key.key,
        algorithms=["RS256"],
        audience=os.environ["AZURE_APP_CLIENT_ID"],
    )
    return claims


def get_user(authorization: Union[str, None] = Header(None)):
    """
    Get currently user detailsfrom authorization header
    """

    if authorization is None:
        return None

    claims = validate_token(authorization)

    try:
        user = User(**claims)
        return user
    except:
        raise HTTPException(
            status_code=400,
            detail=f"Could not parse user from claims. {json.dumps(claims)}",
        )


def check_user_access(user: str, content: str):
    print("check_user_access: ", user)
    return True
