FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
COPY data /app/data

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir .

ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE 8000

CMD ["python", "-m", "ai_schools"]

