FROM ubuntu:18.04 as python3.8
ARG PROJECT_DIR
RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y locales curl python3-distutils python3.8 python3.8-dev \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.8 get-pip.py \
    && rm get-pip.py \
    && pip3.8 install -U pip \
    && mkdir $PROJECT_DIR \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

FROM python3.8 as django
ARG PROJECT_DIR
WORKDIR $PROJECT_DIR
ADD requirements.txt $PROJECT_DIR
RUN pip3.8 install -r requirements.txt
COPY . $PROJECT_DIR

# EXPOSE 8000
# CMD ["python3.8", "manage.py", "runserver", "0.0.0.0:8000"]
