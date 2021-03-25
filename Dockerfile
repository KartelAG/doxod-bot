FROM python:3.9

ADD doxod /doxod
COPY requirements.txt /doxod/requirements.txt

WORKDIR /doxod

RUN pip install -r /doxod/requirements.txt 

ENTRYPOINT ["python", "tg_bot.py"]