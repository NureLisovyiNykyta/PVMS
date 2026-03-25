from fastapi import APIRouter, HTTPException, Query, status
from app.services.string_processor import StringProcessor

router = APIRouter(prefix="/String", tags=["String Operations"])


@router.get("", response_model=str)
async def change_brackets(value: str = Query(None, description="String to Process")):
    res = StringProcessor.change_brackets(value)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erorr: The string is empty or a processing error occurred."
        )

    return res