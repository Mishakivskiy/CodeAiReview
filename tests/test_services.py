import pytest
from app.services.github_service import fetch_repo_contents, get_github_api_url
from app.services.caching_service import get_cached_repo_contents, cache_repo_contents
from unittest.mock import AsyncMock
import httpx


def test_get_github_api_url():
    repo_url = "https://github.com/owner/repo"
    expected_url = "https://api.github.com/repos/owner/repo/contents/"
    assert get_github_api_url(repo_url) == expected_url

    with pytest.raises(ValueError):
        get_github_api_url("https://invalid-url")


@pytest.mark.asyncio
async def test_fetch_repo_contents_from_cache(mocker):
    mocker.patch("app.services.github_service.get_cached_repo_contents", return_value={
        'code_files': ['file1.py', 'file2.py'],
        'files_content': {'file1.py': 'content1', 'file2.py': 'content2'}
    })

    code_files, files_content = await fetch_repo_contents("https://github.com/owner/repo")

    assert code_files == ['file1.py', 'file2.py']
    assert files_content == {'file1.py': 'content1', 'file2.py': 'content2'}


@pytest.mark.asyncio
async def test_fetch_repo_contents_handle_github_error(mocker):
    mocker.patch("app.services.github_service.get_cached_repo_contents", return_value=None)

    mocker.patch("httpx.AsyncClient.get", side_effect=httpx.HTTPStatusError("GitHub error",
                                                                            request=None, response=None))

    with pytest.raises(Exception):
        await fetch_repo_contents("https://github.com/owner/repo")
