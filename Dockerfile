FROM python:3.9-slim-bullseye

RUN groupadd --gid 12345 appuser \
    && useradd --uid 12345 --gid 12345 --system --no-create-home appuser

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app.py /code/

USER appuser

CMD ["python3", "/code/app.py"]
