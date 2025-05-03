FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-cov

# Copy project
COPY . .

# Make run_tests.sh executable
RUN chmod +x run_tests.sh

# Expose port
EXPOSE 80

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]