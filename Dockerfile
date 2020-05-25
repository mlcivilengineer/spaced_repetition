FROM python:3.8-slim
WORKDIR /app

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y --no-install-recommends install wget gnupg gnupg2 gnupg1
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt-get update
RUN apt-get -y --no-install-recommends install google-chrome-stable

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "spaced_repetition.py"]