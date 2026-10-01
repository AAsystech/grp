FROM python:3.13-slim

WORKDIR /app

# Backend dependencies
COPY apps/backend/requirements.txt ./backend-requirements.txt

RUN pip install --no-cache-dir -r backend-requirements.txt

# Database migration dependencies
COPY database/requirements.txt ./database-requirements.txt

RUN pip install --no-cache-dir -r database-requirements.txt

# Application code
COPY apps/backend/app ./app

# Database migration code
COPY database ./database

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]