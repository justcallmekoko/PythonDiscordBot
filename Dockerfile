FROM python:3.8-slim-buster

RUN mkdir -p /var/log/discord_bot

WORKDIR /app

RUN apt-get update && apt-get install -y procps net-tools screen

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Run app directly
CMD [ "python3", "discord_bot.py" ]

# Run app in a screen session via startup script
#CMD [ "startup.sh" ]