FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV FLASK_APP=server.py
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0","--port=1337", "--reload","--debug"]
