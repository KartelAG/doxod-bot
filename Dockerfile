FROM python:3.9

ADD . /src

WORKDIR /src

RUN pip install -r /doxod/requirements.txt 

ENTRYPOINT ["python", "tg_bot.py"]