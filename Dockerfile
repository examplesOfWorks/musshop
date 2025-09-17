FROM python:3.12-slim
RUN groupadd -r groupdjango && useradd -r -g groupdjango usermusshop

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /app/www/musshop
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

USER usermusshop