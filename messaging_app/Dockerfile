# Use Python 3.10 base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose Django default port
EXPOSE 8000   # -p 8000:8000

# Run the Django app using python3
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
