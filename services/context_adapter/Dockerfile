FROM python:3.12-slim
WORKDIR /app

# Install Python dependencies
COPY services/context_adapter/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy service code and shared libraries
COPY services/context_adapter/ .
COPY libs ./libs

# Launch the service with the configured number of workers. Using ``sh -c``
# allows the ``WORKERS`` environment variable to be expanded correctly.
CMD ["sh", "-c", "gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w ${WORKERS:-1} -b 0.0.0.0:8010"]
