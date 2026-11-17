FROM mcr.microsoft.com/playwright/python:v1.56.0-noble
WORKDIR /app
RUN python -m pip install --no-cache-dir playwright==1.56.0
COPY . .
CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]
