FROM pytorch/pytorch

RUN apt-get update -yq \
    && apt-get install curl -y \
    && curl -L https://deb.nodesource.com/setup_12.x | bash \
    && apt-get update -yq \
    && apt-get install -yq \
        nodejs

RUN npm install -g localtunnel

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY modules/ /app/modules
RUN mkdir data
RUN mkdir static
COPY apiEntrypoint.json /app/
COPY app.py /app/
COPY entrypoint.sh /app/
COPY instanceBeacon.py /app/
COPY worker.py /app/

#RUN python modules/download.py

EXPOSE 80

ENTRYPOINT [ "sh", "entrypoint.sh" ]

