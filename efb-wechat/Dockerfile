FROM python:alpine as base

RUN apk add --no-cache tzdata ffmpeg libmagic libwebp cairo && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apk del tzdata && \
    adduser -D efb

FROM base as builder

COPY requirements.txt .

RUN apk add --no-cache build-base openssl-dev zlib-dev jpeg-dev libwebp-dev libffi-dev && \
    python3 -m pip install --upgrade pip

USER efb

RUN pip install --user --no-warn-script-location -r requirements.txt

FROM base

USER efb
WORKDIR /home/efb

COPY --from=builder --chown=efb:efb /home/efb/.local /home/efb/.local
COPY --chown=efb:efb . /home/efb

ENV PATH=/home/efb/.local/bin:${PATH}
ENV EFB_DATA_PATH=/home/efb/efb_config

ENTRYPOINT ["sh", "start.sh"]
