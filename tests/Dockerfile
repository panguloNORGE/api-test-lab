FROM python:3.12-slim
WORKDIR /tests
RUN pip install --no-cache-dir pytest requests
COPY . .
CMD ["pytest", "-v"]