from fastapi import Request


def get_url_service(request: Request):
    return request.app.state.container.get_service()