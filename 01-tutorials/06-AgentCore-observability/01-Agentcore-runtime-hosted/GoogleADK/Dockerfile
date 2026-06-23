FROM public.ecr.aws/docker/library/python:3.14-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache -r pyproject.toml

# ENV OTEL_PYTHON_DISTRO=aws_distro
# ENV OTEL_PYTHON_CONFIGURATOR=aws_configurator
# ENV AGENT_OBSERVABILITY_ENABLED=true

ENV UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_PROGRESS=1 \
    PYTHONUNBUFFERED=1 \
    DOCKER_CONTAINER=1 \
    AWS_REGION=us-east-1 \
    AWS_DEFAULT_REGION=us-east-1

# Create non-root user
RUN useradd -m -u 1000 bedrock_agentcore
USER bedrock_agentcore

COPY ./googleoinftravelctr/ .

EXPOSE 9000
EXPOSE 8000
EXPOSE 8080

CMD ["opentelemetry-instrument", "python", "main.py"]
