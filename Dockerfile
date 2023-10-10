FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

COPY . .

EXPOSE 5001

CMD ["python3", "main.py"]