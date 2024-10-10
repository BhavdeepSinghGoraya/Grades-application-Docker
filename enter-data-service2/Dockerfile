FROM python:3.9

# Set working directory
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# Expose the Flask port (5001 in this case)
EXPOSE 5001

# Run the Flask app
CMD ["python", "app.py"]
