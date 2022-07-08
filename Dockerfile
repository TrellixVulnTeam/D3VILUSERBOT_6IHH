FROM TEAM-D3VIL/d3vilbot:latest

RUN git clone https://github.com/TEAM-D3VIL/D3vilUserbot.git /root/d3vilbot

WORKDIR /root/d3vilbot

RUN pip3 install -U -r requirements.txt

ENV PATH="/home/d3vilbot/bin:$PATH"

CMD ["python3", "-m", "d3vilbot"]
