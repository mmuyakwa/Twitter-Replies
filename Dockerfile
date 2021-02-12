FROM python:3
LABEL maintainer="Michael Muyakwa <mmuyakwa@gmail.com>"

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv shell
RUN pipenv install --ignore-pipfile

WORKDIR /usr/src/app

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD [ "python", "./main.py" ]
