FROM heroku/heroku:20

RUN apt update && apt upgrade -y

RUN apt install git python3-pip -y

RUN pip install fastapi python-docx shortuuid uvicorn

RUN cd /

RUN git clone https://github.com/mkasajim/coverpage-api

RUN cd /coverpage-api

#WORKDIR /app/bin/projects/coverpage-api 

WORKDIR /coverpage-api

CMD python3 api.py
