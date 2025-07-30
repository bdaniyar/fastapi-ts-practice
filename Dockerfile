FROM python:3.11

 RUN mkdir /booking

 WORKDIR /booking

 COPY requirements.txt .

 RUN pip install --no-cache-dir -r requirements.txt

 COPY . .

 RUN chmod a+x /booking/docker/*.sh

 CMD ["./docker/app.sh"]