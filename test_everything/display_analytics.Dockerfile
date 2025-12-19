FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./display_analytics.py /display_analytics.py ./
COPY invokes.py ./
CMD [ "python", "./display_analytics.py" ]