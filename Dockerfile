FROM python:3.10-slim

# environment variables, Prevents Python from creating .pyc files and Makes output logs visible in real time.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# working directory
WORKDIR /app

# Install dependencies to working directory
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . /app/

# 6. Expose port
EXPOSE 8000

# 7. Default command
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "lightrig_api.wsgi:application"]
