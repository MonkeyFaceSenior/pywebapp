# Use official Python slim image
FROM python:3.8-slim

# Set working directory
WORKDIR /api-flask

# Copy necessary files into the directory
COPY flask_blog/ /api-flask/flask_blog/
COPY static/ /api-flask/static/
COPY templates/ /api-flask/templates/
COPY hello.py README test.html flaskenv.txt database.db app.py requirements.txt /api-flask/

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose port 5050 because HomeySRV has a service on 5000 already
EXPOSE 5050

# Set environment variables from flaskenv.txt
RUN set -a && source flaskenv.txt && set +a

# Set the default command to run the Flask app
CMD ["python", "app.py"]