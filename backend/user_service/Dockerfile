# Step 1: Use an official Python image as the base image
FROM python:3.12.6-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy the requirements file to the working directory
COPY user_service/requirements.txt .
# Step 6: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Copy the application source code to the container
COPY user_service/ .

# Step 8: Expose the port your app runs on
EXPOSE 8000

# Step 9: Define the command to run your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
