from app.services.caching_service import cache_repo_contents, get_cached_repo_contents
import httpx
from app.core.config import GITHUB_TOKEN


def get_github_api_url(repo_url: str) -> str:
    repo_parts = repo_url.strip('/').split('/')

    if len(repo_parts) < 2 or repo_parts[2] != 'github.com':
        raise ValueError("Error URL GitHub.")

    api_url = f"https://api.github.com/repos/{repo_parts[3]}/{repo_parts[4]}/contents/"
    return api_url


async def fetch_repo_contents(github_repo_url: str):
    cached_contents = await get_cached_repo_contents(github_repo_url)
    if cached_contents:
        return cached_contents['code_files'], cached_contents['files_content']

    async with httpx.AsyncClient() as client:
        try:
            github_repo_url = get_github_api_url(github_repo_url)
            print(github_repo_url)
            headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
            response = await client.get(github_repo_url, headers=headers)
            response.raise_for_status()

            contents = response.json()
            code_files = []
            files_content = {}

            for item in contents:
                if item['type'] == 'file':
                    code_files.append(item['download_url'])
                elif item['type'] == 'dir':
                    subfolder_url = item['url']
                    sub_code_files, sub_files_content = await fetch_repo_contents(subfolder_url)
                    code_files.extend(sub_code_files)
                    files_content.update(sub_files_content)

            for file_url in code_files:
                try:
                    file_response = await client.get(file_url, headers=headers)
                    file_response.raise_for_status()
                    files_content[file_url] = file_response.text
                except httpx.HTTPStatusError as e:
                    print(f"Failed to fetch file content: {file_url}. Error: {e}")

            await cache_repo_contents(github_repo_url, {
                'code_files': code_files,
                'files_content': files_content
            })

            return code_files, files_content

        except httpx.HTTPStatusError as e:
            raise Exception(f"An error occurred while requesting the repository: {e}")
        except httpx.RequestError as e:
            raise Exception(f"An error occurred while making the request: {e}")
        except ValueError as e:
            raise Exception(f"Failed to parse response as JSON: {e}")
