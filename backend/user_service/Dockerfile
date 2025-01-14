# Step 1: Use an official Python image
FROM python:3.12-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Set the working directory
WORKDIR /app

# Step 4: Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy the requirements file
COPY user_service/requirements.txt /app/

# Step 6: Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Copy the application source code
COPY . /app/

# Step 8: Expose the application port
EXPOSE 8000

# Step 9: Set the command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
