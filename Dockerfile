FROM python:3.12-slim


# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1  
     
# Ensure output is logged in real-time
ENV PYTHONUNBUFFERED=1   

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all files from the current directory into the container
COPY . .

# Install testing dependencies
RUN pip install pytest pytest-mock

# Expose the default Streamlit port
EXPOSE 8501

# Default command to run Streamlit app
CMD ["streamlit", "run", "app.py"]
