FROM python:3.11-slim
WORKDIR /app
COPY main.py .
CMD ["python", "leetcode_2.py"]