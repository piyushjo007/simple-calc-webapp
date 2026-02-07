FROM python:3.11-slim as build

RUN useradd -m appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app
USER appuser

RUN pytest tests/
# Stage 2: Production image

FROM python:3.11-slim

RUN useradd -m appuser
WORKDIR /app

COPY --from=build /app .

RUN chown -R appuser:appuser /app
USER appuser


EXPOSE 8080

CMD ["python3", "main.py"]
