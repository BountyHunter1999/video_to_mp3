import os
import requests


def token(request):
    """Validate the JWT token send by the client"""
    if "Authorization" not in request.headers:
        return None, ("Missing Credentials", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("Missing Credentials", 401)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        # response.text will have the body the access that this token has
        return response.text, None
    else:
        return None, (response.text, response.status_code)
