FROM python:3.9-slim

WORKDIR /app
COPY . /app
RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry install

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
