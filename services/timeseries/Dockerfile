FROM python:3.12-slim
WORKDIR /app

# Install Python dependencies
COPY services/timeseries/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code and shared libraries
COPY services/timeseries/ .
COPY libs ./libs

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8020"]
