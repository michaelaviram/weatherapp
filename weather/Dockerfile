#stage1: building the enviroment
FROM python:3.11-slim AS builder
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
ENV BG_COLOR="powderblue"

#stage3: building the runtime
FROM builder AS runtime
CMD ["gunicorn", "-b", "0.0.0.0:8989", "wsgi:app"]

