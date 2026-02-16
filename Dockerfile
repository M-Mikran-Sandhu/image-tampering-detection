# Use a base image with both Node.js and Python
FROM node:18-alpine

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY requirements.txt .

# Install Node.js dependencies
RUN npm install

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Build the React frontend
RUN npm run build

# Expose port
EXPOSE 5000

# Set environment variable for production
ENV ENVIRONMENT=production
ENV RAILWAY_DEPLOYMENT=true

# Run the Flask application
CMD ["python", "app.py"]