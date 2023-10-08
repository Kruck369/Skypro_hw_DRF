FROM python

WORKDIR /drf_hw

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver"]
