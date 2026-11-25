FROM python:3.15-slim
WORKDIR /app
RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY . .
EXPOSE 8000
CMD ["python", "newproject/manage.py", "runserver", "0.0.0.0:8000"]
