FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp/
RUN apt-get update \
    && apt-get install gcc libpq-dev -y \
    && apt-get clean \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt
ENV PROJECT_ROOT /project
ENV PATH $PATH:$PROJECT_ROOT
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT