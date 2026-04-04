# Use official python image
FROM python:3.11-slim

# set working directory
WORKDIR /app

# copy project files
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# DO NOT hardcode port
# (optional but safe)
EXPOSE 8080

# run with dynamic Railway port
CMD ["sh", "-c", "gunicorn wsgi:app --bind 0.0.0.0:$PORT"]