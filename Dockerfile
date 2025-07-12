# REM-CODE Lite Docker Container
# Constitutional Programming Language for AI Governance and Democratic Multi-Agent Systems

FROM python:3.11-slim

LABEL maintainer="Jayne Yu <jayneyu@example.com>"
LABEL description="REM-CODE Lite - Constitutional Programming Language"
LABEL version="2.4.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV REM_CODE_VERSION=2.4.0
ENV REM_CODE_MODE=production

# Create non-root user for security
RUN groupadd -r remcode && useradd -r -g remcode remcode

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional packages for interactive features
RUN pip install --no-cache-dir \
    rich>=12.0.0 \
    jupyter>=1.0.0 \
    ipython>=8.0.0

# Copy the application code
COPY . .

# Install REM-CODE Lite in development mode
RUN pip install -e .

# Create directories for data and logs
RUN mkdir -p /app/data /app/logs /app/examples /app/user_programs
RUN chown -R remcode:remcode /app

# Switch to non-root user
USER remcode

# Copy constitutional examples to user accessible location
COPY --chown=remcode:remcode examples/ /app/examples/

# Create entrypoint script
RUN echo '#!/bin/bash\n\
if [ "$1" = "tutorial" ]; then\n\
    python interactive_tutorial.py\n\
elif [ "$1" = "shell" ]; then\n\
    python -m shell.rem_shell\n\
elif [ "$1" = "web" ]; then\n\
    python -m shell.rem_web_shell --port ${PORT:-8080}\n\
elif [ "$1" = "gui" ]; then\n\
    python -m gui.rem_gui\n\
elif [ "$1" = "dashboard" ]; then\n\
    python rem_dashboard.py --port ${PORT:-8081}\n\
elif [ "$1" = "examples" ]; then\n\
    echo "Running constitutional programming examples:"\n\
    for example in /app/examples/*.remc; do\n\
        echo "Running $(basename $example)"\n\
        python -m shell.rem_shell "$example"\n\
    done\n\
elif [ "$1" = "demo" ]; then\n\
    python constitutional/error_demo.py\n\
elif [ "$1" = "jupyter" ]; then\n\
    jupyter notebook --ip=0.0.0.0 --port=${PORT:-8888} --no-browser --allow-root\n\
else\n\
    exec "$@"\n\
fi' > /app/docker-entrypoint.sh && chmod +x /app/docker-entrypoint.sh

# Expose ports for web interfaces
EXPOSE 8080 8081 8888

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import constitutional; print('REM-CODE Lite healthy')" || exit 1

# Set default entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default command shows help
CMD ["tutorial"]