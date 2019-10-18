FROM python:3.7

ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR "/tmp"

COPY truetype/ /usr/share/fonts/truetype/suisse/

COPY . /tmp

RUN fc-cache -fv && python3 -m pip install -r requirements.txt

EXPOSE 8080

CMD ["python3", "/tmp/main.py"]