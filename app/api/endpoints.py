import json
from fastapi import APIRouter, HTTPException
from app.services.github_service import fetch_repo_contents
from app.services.openai_service import analyze_code
from app.models.request_model import ReviewRequest
from app.models.response_model import ReviewResponse

review_router = APIRouter()


@review_router.post("/review", response_model=ReviewResponse)
async def review_code(request: ReviewRequest):
    try:
        repo_files, files_with_content = await fetch_repo_contents(request.github_repo_url)
        clear_repo_files = []
        for file in repo_files:
            clear_repo_files.append(file.split('/')[-1])

        review_result = await analyze_code(
            files_with_content,
            request.assignment_description,
            request.candidate_level,
            request.openai_token,
        )

        review_result = json.loads(review_result.replace('```json', '').replace('```', ''))

        return ReviewResponse(
            found_files=clear_repo_files,
            downsides=review_result["downsides"],
            rating=review_result["rating"],
            conclusion=review_result["conclusion"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
