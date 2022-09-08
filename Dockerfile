# 파이썬에서 알파인 이미지가 제일 가볍다.
FROM python:3.9-alpine3.13

# 누가 유지보수 했는지 명시해준다.
LABEL maintainer="soyuly"

# 로그를 즉시 볼 수 있다.
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8000

ARG DEV=false

# 가상환경을 만들고, requirements를 설치한다.
# 컨테이너안에 루트 유저를 만든다
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "${DEV}" = "true"] ; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# 환경변수 설정해주는 것
ENV PATH="/py/bin:$PATH"

# 모든 루트권한을 제거해서 보안을 강화시키기
USER django-user 