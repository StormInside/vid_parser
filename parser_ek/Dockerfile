FROM debian

RUN apt update
RUN apt install python3 python3-pip -y
RUN pip3 install bs4 requests

COPY . /parsers

CMD python3 /parsers/parser_ek.py > output.txt
