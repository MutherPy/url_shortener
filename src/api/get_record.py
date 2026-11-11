from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException
from src.api.deps import get_url_service
from src.application.domain.exc.domain_exc import NotFoundException
from src.ports.domain.service_port import IUrlService
from starlette import status
from starlette.responses import RedirectResponse

router = APIRouter()

@router.get("/{code}",
            status_code=302,
            response_class=RedirectResponse,
    responses={
        302: {
            "description": "Redirect to original URL",
            "headers": {
                "Location": {
                    "description": "Original URL",
                    "schema": {
                        "type": "string",
                        "format": "uri",
                    },
                },
            },
        },
    },
)
async def get_record(code: str, url_service: Annotated[IUrlService, Depends(get_url_service)]):
    try:
        original_url = await url_service.get(code)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_302_FOUND, headers={"Location": original_url})