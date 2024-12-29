
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install pymongo
EXPOSE 3000 5000

CMD ["sh", "-c", "python3 socket_server.py & python3 main.py"]
