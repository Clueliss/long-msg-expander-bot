FROM docker.io/fedora

ENV LONG_MSG_EXPANDER_DISCORD_TOKEN=YOUR_BOT_TOKEN

RUN dnf install python3 python3-pip git -y
RUN python3 -m pip install discord requests

RUN curl -sSf https://raw.githubusercontent.com/Clueliss/long-msg-expander-bot/master/long-msg-expander.py > /init
RUN chmod +x /init

CMD ["/init"]
