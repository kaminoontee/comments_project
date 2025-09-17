# 1. Stage: Build frontend

FROM node:22-alpine AS frontend-build

WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build


# 2. Stage: Backend + Final
FROM python:3.10-slim AS backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

# requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# скопировать Django проект
COPY comments_app/ ./comments_app

# скопировать собранный фронтенд в static
COPY --from=frontend-build /frontend/dist ./frontend_dist

# entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
CMD ["/app/entrypoint.sh"]
