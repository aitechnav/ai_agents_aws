FROM public.ecr.aws/docker/library/python:3.12-slim

# Set working directory to /app/src
WORKDIR /app/src

# Copy source code and requirements into container
COPY src/ /app/src

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set AWS region (required for Bedrock SDK access)
ENV AWS_REGION=us-east-1
ENV AWS_DEFAULT_REGION=us-east-1


# Create non-root user
RUN useradd -m -u 1000 bedrock_agentcore
USER bedrock_agentcore

EXPOSE 8080

# Start the agent
CMD ["python", "agent.py"]
