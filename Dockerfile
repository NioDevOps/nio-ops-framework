FROM python:3.7
RUN mkdir -p /app/nio-ops-framework/
ADD cmdb /app/nio-ops-framework/
ADD requirements.txt /app/nio-ops-framework/
ADD manage.py /app/nio-ops-framework/


COPY cmdb /app/nio-ops-framework/
COPY manage.py /app/nio-ops-framework/
COPY requirements.txt /app/nio-ops-framework/requirements.txt
WORKDIR /app/nio-ops-framework/
RUN pip install -r /app/nio-ops-framework/requirements.txt
CMD python manager runserver 0.0.0.0:8000
EXPOSE 8000