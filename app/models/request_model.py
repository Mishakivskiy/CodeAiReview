from pydantic import BaseModel, Field

class ReviewRequest(BaseModel):
    assignment_description: str = Field(..., description="Description of the coding assignment.")
    github_repo_url: str = Field(..., description="URL of the GitHub repository to review.")
    candidate_level: str = Field(..., pattern="^(Junior|Middle|Senior)$", description="Candidate's level.")
    openai_token: str = Field(..., description="OpenAI api token")