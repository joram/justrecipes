#!/usr/bin/env python3
from fastapi import HTTPException, Header
from google.oauth2 import id_token
from google.auth.transport import requests

# (Receive token by HTTPS POST)
# ...

CLIENT_ID = "184422986756-mneassqbhd7nsrbdmtbjcbped1kfi234.apps.googleusercontent.com"


def verify_jwt(token:str) -> bool:
    try:
        id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        return True
    except Exception as e:
        print(e)
        pass
    return False

def get_email(jwt: str) -> str:
    try:
        info = id_token.verify_oauth2_token(jwt, requests.Request(), CLIENT_ID)
        email = info.get("email", None)
        if email:
            return email
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid JWT {e}")
    raise HTTPException(status_code=401, detail=f"Invalid JWT")


def get_jwt(jwt: str = Header(...)):
    is_valid = verify_jwt(jwt)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid JWT")
    return jwt


if __name__ == "__main__":
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjkxNDEzY2Y0ZmEwY2I5MmEzYzNmNWEwNTQ1MDkxMzJjNDc2NjA5MzciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxODQ0MjI5ODY3NTYtbW5lYXNzcWJoZDduc3JiZG10YmpjYnBlZDFrZmkyMzQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIxODQ0MjI5ODY3NTYtbW5lYXNzcWJoZDduc3JiZG10YmpjYnBlZDFrZmkyMzQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDUxMDU5MTk4NjM5MjMyNTgxMzUiLCJlbWFpbCI6ImpvaG4uYy5vcmFtQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYmYiOjE3MDQ1NzYwMDUsIm5hbWUiOiJKb2huIE9yYW0iLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTGFkbmFXcm9IUVlmcF80UXRobkFLd1k2UklPT0RrSHB4UHZTVGtxdVkyTTBUUj1zOTYtYyIsImdpdmVuX25hbWUiOiJKb2huIiwiZmFtaWx5X25hbWUiOiJPcmFtIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE3MDQ1NzYzMDUsImV4cCI6MTcwNDU3OTkwNSwianRpIjoiNzA2Y2JkMDM4MDg2NWQ1MGMyODVmM2VmOTEwMDgzM2NmZTJiMTk0YSJ9.g7xok2cmYlwBFHNjX-ZEtPYjRMEbsRFMjx1Gp4MioyS47PjchgxQloAX7jH9raS7h8CIZL0pOF-krmmn7CRbArK25B9MsyVISR9HKmHPsu8FaAQqtG5rYUVTN-Bt1guyiJUVKtdF6sB0IanYfUBsmTJhaVAKtF6MPtaibmN-Y6ZeGMillIryg-BcDjCwcNCG7fdOkf0Ht17L4z5ZqETcrOhkZ-cXsMYfxz-B1yfG2WdulxPa4UPnGpcwPXAzZ7doOaJ0pXW52EK5DKnmfn0nT08jg9l_bWvIAKfUu-l9nEUZrlYM-XOqLiUqqv2WlLvemeLaftiS8zvXTukkLmCYXw"
    results = verify_jwt(token)
    print(results)