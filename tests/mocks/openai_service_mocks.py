import pytest


@pytest.fixture
def mock_openai_response(mocker):
    mocker.patch(
        "app.services.openai_service.analyze_code",
        return_value={
            "files": ["main.py"],
            "comments": ["Code is not modular enough."],
            "rating": 4,
            "conclusion": "Good, but improvements needed."
        },
    )
