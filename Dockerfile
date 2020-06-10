FROM python:3.5.2
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN apt-get update -y && apt-get install -y python-pip python-dev
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
ONBUILD COPY requirements.txt /usr/src/app/
ONBUILD RUN pip install --no-cache-dir -r requirements.txt
ONBUILD COPY . /usr/src/app
WORKDIR /usr/src/app
RUN python ./manage.py collectstatic
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8014" ]

