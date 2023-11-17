FROM python:3.12.0

COPY ./ ./

RUN pip install --no-cache-dir --upgrade -r requirement.txt

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]