FROM python:3.9

ADD src /doxod/src
COPY requirements.txt /doxod/requirements.txt

WORKDIR /doxod/src

RUN pip install -r /doxod/requirements.txt 

ENTRYPOINT ["python", "tg_bot.py"]