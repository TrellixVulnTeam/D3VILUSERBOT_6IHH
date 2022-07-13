FROM TEAM-D3VIL/D3vilBot:latest

RUN git clone https://github.com/D3KRISH/D3vilUserbot.git /root/d3vilbot

WORKDIR /root/d3vilbot

RUN pip3 install -U -r requirements.txt

ENV PATH="/home/d3vilbot/bin:$PATH"

CMD ["python3", "-m", "d3vilbot"]
