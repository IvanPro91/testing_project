FROM python:3.9
WORKDIR /testing_project
ADD . /testing_project
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
ENV MODE=dev
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["python", "./run.py"]