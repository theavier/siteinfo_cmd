FROM python:3.9-alpine

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV APP_ROOT /code
ENV CONFIG_ROOT /config

# set work directory
RUN mkdir ${CONFIG_ROOT}
RUN mkdir ${APP_ROOT}

# install dependencies
RUN apk update && apk add postgresql-dev gcc
RUN pip install --upgrade pip
WORKDIR ${CONFIG_ROOT}
#COPY requirements.txt ${CONFIG_ROOT}/
COPY requirements.txt .
RUN pip install -r ${CONFIG_ROOT}/requirements.txt
RUN pip install uvicorn
#RUN apk update && apk add cron

# copy project
WORKDIR ${APP_ROOT}
COPY . .
#run application
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]