import pytest


@pytest.fixture
def mock_github_response(mocker):
    mocker.patch(
        "app.services.github_service.fetch_repo_contents",
        return_value=[{"filename": "main.py", "content": "print('Hello, World!')"}],
    )
