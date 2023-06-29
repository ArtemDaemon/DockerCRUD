FROM python
RUN pip install mysql-connector-python
RUN pip install pymongo
RUN pip install docker
WORKDIR /usr/app/src
COPY main.py ./
COPY data.csv ./
COPY MySQL.py ./
COPY MongoDB.py ./
EXPOSE 27017