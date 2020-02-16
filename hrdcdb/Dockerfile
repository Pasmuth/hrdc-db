FROM gcr.io/hrdc-db/flask-base
COPY app app
COPY migrations migrations
COPY hrdcdb.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP hrdcdb.py

ENTRYPOINT ["bash","./boot.sh"]