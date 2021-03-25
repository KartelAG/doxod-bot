FROM python:3.9

ADD . /src

WORKDIR /src

RUN pip install -r /src/requirements.txt 

ENV TZ=Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENTRYPOINT ["python", "tg_bot.py"]