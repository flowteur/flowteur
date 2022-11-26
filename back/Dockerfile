FROM pytorch/pytorch

WORKDIR /app

COPY ./ /app/

RUN pip install -r requirements.txt

RUN python modules/download.py

ENTRYPOINT [ "sh", "entrypoint.sh" ]

EXPOSE 5000