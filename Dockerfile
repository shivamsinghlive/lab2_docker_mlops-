FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY src/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py ./main.py

RUN useradd --create-home --uid 10001 app \
    && mkdir -p /app/artifacts \
    && chown -R app:app /app

USER app

ENTRYPOINT ["python", "main.py"]
CMD ["--output", "/app/artifacts/iris_model.joblib"]
