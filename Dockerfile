# Use Python 3.10 as the base image
FROM python:3.10

# Set the working directory
WORKDIR /code

# Copy requirements and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the necessary project directories
COPY ./data /code/data
COPY ./models /code/models
COPY ./src /code/src

# Create a writable directory for cache if needed (optional but good practice)
RUN mkdir -p /code/data/cache && chmod -R 777 /code/data/cache

# Run the application on port 7860 (Hugging Face default)
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
