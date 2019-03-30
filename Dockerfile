FROM python:3.6-jessie as base
# TA-lib is required by the python TA-lib wrapper. This provides analysis.
COPY lib/ta-lib-0.4.0-src.tar.gz /tmp/ta-lib-0.4.0-src.tar.gz

RUN cd /tmp && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

COPY app/requirements-step-1.txt .
COPY app/requirements-step-2.txt .

RUN pip install -r requirements-step-1.txt
RUN pip wheel --wheel-dir=/wheelhouse -r /requirements-step-1.txt
RUN pip wheel --wheel-dir=/wheelhouse -r /requirements-step-2.txt

RUN ls -la /usr/lib

FROM python:3.6-slim

COPY --from=base /usr/include/ta-lib /usr/include/ta-lib
COPY --from=base /usr/lib/libta_lib.* /usr/lib/

COPY --from=base /wheelhouse /wheelhouse

ADD app/ /app
WORKDIR /app

RUN pip install --no-index --find-links=/wheelhouse -r requirements-step-1.txt
RUN pip install --no-index --find-links=/wheelhouse -r requirements-step-2.txt

CMD ["/usr/local/bin/python","app.py"]
