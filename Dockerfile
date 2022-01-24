FROM python:3.9

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY . .

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]


# 도커세팅 참고
# https://malwareanalysis.tistory.com/139
# https://fastapi.tiangolo.com/deployment/docker/