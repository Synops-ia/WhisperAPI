FROM pytorch/pytorch:2.1.1-cuda12.1-cudnn8-runtime

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
