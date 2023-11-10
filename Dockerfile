FROM python:3.11.5-slim as build

ENV VIRTUAL_ENV=/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt update && apt install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libcurl4-openssl-dev \
    gcc \
 && apt clean \
 && rm -rf /var/lib/apt/lists/*

# Update pip
RUN pip install --upgrade pip

# Install packages
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

FROM python:3.11.5-slim

COPY --from=build /venv /venv

ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . /app
COPY ./database_healthcheck.sh /tmp/
WORKDIR /app
ENTRYPOINT ["bash", "/tmp/database_healthcheck.sh"]

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000

