FROM python:3.12-slim

WORKDIR /app

# 设置国内PyPI镜像，加速安装
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
ENV PIP_TRUSTED_HOST=mirrors.aliyun.com
ENV PIP_TIMEOUT=120

# 安装系统依赖（用于编译某些Python包）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 先复制requirements.txt，利用Docker缓存
COPY requirements.txt .

# 安装Python依赖，增加超时时间
RUN pip install --no-cache-dir --timeout=120 -r requirements.txt

# 复制项目文件
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
