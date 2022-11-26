FROM pytorch/pytorch

WORKDIR /app

COPY ./ /app/

RUN pip install -r requirements.txt

ENTRYPOINT [ "sh", "entrypoint.sh" ]

EXPOSE 5000