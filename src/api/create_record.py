from fastapi import APIRouter, Depends, HTTPException
from src.api.deps import get_url_service
from src.api.dto import UrlInput, UrlOutput
from src.application.domain.exc.domain_exc import CodeGenerationError
from src.ports.domain.dto import UrlCreateDomainDTO
from src.ports.domain.service_port import IUrlService
from starlette import status
from typing import Annotated

router = APIRouter(prefix="/api/v1")

@router.post("/urls", status_code=status.HTTP_201_CREATED, response_model=UrlOutput)
async def create_record(url: UrlInput, url_service: Annotated[IUrlService, Depends(get_url_service)]):
    url_dto = UrlCreateDomainDTO(
        original_url=str(url.url)
    )
    try:
        result = await url_service.create(url_dto=url_dto)
    except CodeGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to create a short URL. Please try again.",
        ) from exc
    return UrlOutput(
        short_code=result.code,
        short_url=result.short_url
    )
