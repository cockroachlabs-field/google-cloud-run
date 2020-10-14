
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
ENV COCKROACH_URI postgres://chris@clerk-test-5th.gcp-us-east4.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=/app/certs/clerk-test-ca.crt
ENV COCKROACH_HOST clerk-test-5th.gcp-us-east4.cockroachlabs.cloud
ENV COCKROACH_PORT 26257
ENV COCKROACH_DB defaultdb
ENV COCKROACH_USER chris
ENV COCKROACH_SSLMODE verify-full
ENV COCKROACH_ROOTCERT /app/certs/clerk-test-ca.crt
ENV COCKROACH_PASS cockroach1234
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install Flask gunicorn
RUN pip install psycopg2-binary
#RUN pip install cockroachdb

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :8080 --workers 1 --threads 4 --timeout 0 main:app