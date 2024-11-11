FROM ubuntu:22.04
LABEL authors="zxasv"
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# install app dependencies
RUN apt-get update  \
    && apt update  \
    && apt upgrade
RUN apt-get install -y curl jq
RUN apt install -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa  \
    && apt update
RUN apt install -y python3.13\
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1\
    && update-alternatives --config python3 \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.13
RUN apt-get install -y git ffmpeg libsm6 libxext6
RUN [ "sh", "-c", "python3 --version" ]
RUN [ "sh", "-c", "pip3 --version" ]
RUN [ "sh", "-c", "git --version" ]
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip -r /app/requirements.txt
RUN [ "sh", "-c", "ls" ]
EXPOSE 5000
ENTRYPOINT ["python3", "/app/main.py"]
