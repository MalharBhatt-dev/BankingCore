FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# 🔥 VERY IMPORTANT
ENV PORT=8080

EXPOSE 8080

CMD gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120