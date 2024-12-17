from fastapi import FastAPI
from app.api.endpoints import review_router
from app.core.logging import logger

app = FastAPI(title="CodeReviewAI")
app.include_router(review_router, prefix="/api/v1")

logger.info("Starting CodeAiReview application...")
