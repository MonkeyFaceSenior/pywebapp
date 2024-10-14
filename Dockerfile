# Use official Python slim image
FROM python:3.8-slim

# set working dir
WORKDIR /api-flask

#copy necessary fies  into the dir
COPY flask_blog/ static/ templates/ hello.py README test.html flaskenv.txt database.db app.py requirements.txt /api-flask/
COPY flask_blog/ /api-flask/flask_blog/
COPY static/ /api-flask/static/
COPY templates/ /api-flask/templates/
#COPY hello.py README test.html app.py requirements.txt databse.db test.html /api-flask/

# upgrade ip and install py dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# expose port 5001
EXPOSE 5001

# run flask on non standard port 5001
CMD ["flask","-e","flaskenv.txt", "run"]