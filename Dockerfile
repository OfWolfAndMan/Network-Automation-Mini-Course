FROM python:3.7
MAINTAINER Anthony

ENV INSTALL_PATH /net-auto
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

