# 使用官方的 Python 3.9 镜像作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到工作目录
COPY . /app

# 安装所需的包
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir Flask request uuid

# 暴露容器的端口
EXPOSE 5000

# 运行 Flask 应用
CMD ["python", "app.py"]
