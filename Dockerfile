FROM alpine

# 容器默认时区为UTC，如需使用上海时间请启用以下时区设置命令
# RUN apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tencent.com/g' /etc/apk/repositories \
&& apk add --update --no-cache python3 py3-pip gcc python3-dev ca-certificates\
&& rm -rf /var/cache/apk/*

COPY . /app
WORKDIR /app

RUN python -m venv /app/venv \
&& . /app/venv/bin/activate
ENV PATH="/app/venv/bin:$PATH"
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple \
&& pip config set global.trusted-host mirrors.cloud.tencent.com \
&& pip install --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt \

# 暴露端口
# 此处端口必须与「服务设置」-「流水线」以及「手动上传代码包」部署时填写的端口一致，否则会部署失败。
EXPOSE 80

CMD ["sh", "start.sh"]
