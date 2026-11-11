from fastapi import APIRouter, Depends
from src.api.deps import get_url_service
from src.api.dto import UrlInput, UrlOutput
from src.ports.domain.dto import UrlCreateDomainDTO
from src.ports.domain.service_port import IUrlService
from starlette import status
from typing import Annotated

router = APIRouter(prefix="/api/v1")

@router.post("/urls", status_code=status.HTTP_201_CREATED, response_model=UrlOutput)
async def create_record(url: UrlInput, url_service: Annotated[IUrlService, Depends(get_url_service)]):
    url_dto = UrlCreateDomainDTO(
        original_url=url.url
    )
    result = await url_service.create(url_dto=url_dto)
    return UrlOutput(
        short_code=result.code,
        short_url=result.short_url
    )
