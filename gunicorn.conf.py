
# opentelemetry auto instrumentation doesn’t work well with application servers (Gunicorn, uWSGI) 
# which are based on the pre-fork web server model. 
# https://opentelemetry-python.readthedocs.io/en/latest/examples/fork-process-model/README.html#working-with-fork-process-models

# Github Issues:
# https://github.com/open-telemetry/opentelemetry-python-contrib/issues/2086
# https://github.com/open-telemetry/opentelemetry-python/issues/2038
# https://github.com/open-telemetry/opentelemetry-python/issues/3573

# for gunicorn, we can use the post_fork hook to initialize the auto instrumentation in each worker process.

# --- Gunicorn Hook ---
def post_fork(server, worker):
    # https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/opentelemetry-instrumentation#programmatic-auto-instrumentation
    from opentelemetry.instrumentation import auto_instrumentation
    auto_instrumentation.initialize()

    worker.log.info(f"Worker {worker.pid} is auto instrumented with OpenTelemetry.")