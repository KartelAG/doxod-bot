FROM python:3.9

ADD src /doxod/src
COPY requirements.txt /doxod/requirements.txt

WORKDIR /doxod/src

RUN pip install -r /doxod/requirements.txt 

ENV TZ=Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENTRYPOINT ["python", "tg_bot.py"]