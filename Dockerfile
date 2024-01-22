ARG openai_api_key

FROM pytorch/pytorch:2.1.1-cuda12.1-cudnn8-runtime

WORKDIR /app

COPY . /app

ENV OPENAI_API_KEY=$openai_api_key

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
