# Use official python image
FROM python:3.11-slim

# set working directory
WORKDIR /app

# copy project files
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose correct port (IMPORTANT)
EXPOSE 8000

# run with gunicorn using Railway PORT
CMD ["sh", "-c", "gunicorn wsgi:app --bind 0.0.0.0:${PORT:-8000}"]