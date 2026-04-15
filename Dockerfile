# base image
FROM python:3.13-slim-bookworm AS base

WORKDIR /app/api

# Install uv
ENV UV_VERSION=0.8.9

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set global.trusted-host mirrors.aliyun.com

RUN pip install --no-cache-dir uv==${UV_VERSION}

FROM base AS packages

RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml uv.lock ./
# RUN uv sync --locked --no-dev --default-index https://pypi.tuna.tsinghua.edu.cn/simple
RUN uv sync --no-dev --default-index https://pypi.tuna.tsinghua.edu.cn/simple

# production stage
FROM base AS production

RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates gnupg2 \
      unixodbc unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
      > /etc/apt/sources.list.d/microsoft-prod.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

ENV FLASK_APP=app.py
ENV DEPLOY_ENV=PRODUCTION

EXPOSE 5001

# set timezone
ENV TZ=UTC

# Set UTF-8 locale
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PYTHONIOENCODING=utf-8

WORKDIR /app/api

# Create non-root user
ARG admin_uid=1001
RUN groupadd -r -g ${admin_uid} admin && \
    # 关键：加 -m 自动创建家目录 /home/admin
    useradd -r -m -u ${admin_uid} -g ${admin_uid} -s /bin/bash admin && \
    chown -R admin:admin /app && \
    # 授权家目录
    chown -R admin:admin /home/admin

# Copy Python environment and packages
ENV VIRTUAL_ENV=/app/api/.venv
COPY --from=packages --chown=admin:admin ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Copy source code
COPY --chown=admin:admin . /app/api/

# Prepare entrypoint script
COPY --chown=admin:admin --chmod=755 docker/entrypoint.sh /entrypoint.sh

USER admin

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]