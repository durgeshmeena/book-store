# Build the virtualenv as a separate step: Only re-execute this step when requirements.txt changes
FROM python:3.11-slim AS build-venv
COPY requirements.txt /requirements.txt
RUN ln -s /usr/local/bin/python3 /usr/bin/python3 && \
    /usr/bin/python3 -m venv /venv && \
    /venv/bin/pip install --disable-pip-version-check -r /requirements.txt && \
    /venv/bin/pip install --disable-pip-version-check opentelemetry-distro opentelemetry-exporter-prometheus && \
    /venv/bin/opentelemetry-bootstrap -a install

# Copy the virtualenv into a distroless image
FROM gcr.io/distroless/python3-debian12:nonroot AS runtime
ENV PATH="/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1
COPY --from=build-venv /venv /venv
COPY . /application
WORKDIR /application

USER nonroot

EXPOSE 8000
ENTRYPOINT ["gunicorn"]
CMD ["app:app", "--bind=0.0.0.0:8000"]