import pytest
from httpx import AsyncClient, ASGITransport
from main import app

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("test")


@pytest.mark.asyncio
async def test_review_success(mocker):
    mocker.patch(
        "app.services.github_service.fetch_repo_contents",
        return_value=[
            {"filename": "main.py", "content": "print('Hello, World!')"},
            {"filename": "utils.py", "content": "def helper(): pass"},
        ]
    )

    mocker.patch(
        "app.services.openai_service.analyze_code",
        return_value={
            "files": ["main.py", "utils.py"],
            "comments": ["Code is well-structured but could use more comments."],
            "rating": 8,
            "conclusion": "Good work overall.",
        }
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/review",
            json={
                "assignment_description": "Implement a REST API",
                "github_repo_url": "https://github.com/Mishakivskiy/for_viewing",
                "candidate_level": "Junior",
                "openai_token": "valid-token"
            },
        )
        logger.debug(f"Response status: {response.status_code}, body: {response.text}")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_review_invalid_url():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/review",
            json={
                "assignment_description": "Implement a REST API",
                "github_repo_url": "https://github.com/invalid/repo",
                "candidate_level": "Junior",
                "openai_token": "valid-token"
            },
        )

    assert response.status_code == 500


@pytest.mark.asyncio
async def test_review_github_error(mocker):
    mocker.patch(
        "app.services.github_service.fetch_repo_contents",
        side_effect=Exception("GitHub error")
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/review",
            json={
                "assignment_description": "Implement a REST API",
                "github_repo_url": "https://github.com/Mishakivskiy/for_viewing",
                "candidate_level": "Junior",
                "openai_token": "valid-token"
            },
        )

    assert response.status_code == 500
