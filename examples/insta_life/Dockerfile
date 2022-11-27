FROM python
RUN apt update && apt install git -y

WORKDIR /app

COPY  ./  .

RUN pip install -r requirements.txt

ENTRYPOINT [ "sh", "entrypoint.sh" ]