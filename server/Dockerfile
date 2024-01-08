FROM public.ecr.aws/lambda/python:3.12

WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD . /app

CMD [ "main.handler" ]