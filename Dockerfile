# Use official python image
FROM python:3.11-slim

# set working directory
WORKDIR /app

# copy project files..
COPY . .

# install dependencies...
RUN pip install --no-cache-dir -r requirements.txt

# expose port
EXPOSE 5000

#run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:create_app()"]