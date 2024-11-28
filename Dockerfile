# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY api /app/api
COPY app /app/app
COPY requirements.txt /app/requirements.txt
COPY .env /app/.env
# Install dependencies for both services
RUN pip install --no-cache-dir -r /app/requirements.txt

# Default command (run Flask and Streamlit together)
CMD ["sh", "-c", "cd /app/api && python api.py & cd /app/app && streamlit run app.py --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false"]
