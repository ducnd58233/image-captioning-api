FROM python:3.9-slim

WORKDIR /app

COPY . /app

EXPOSE 30000

RUN pip install -r requirements.txt --no-cache-dir
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "30000"]