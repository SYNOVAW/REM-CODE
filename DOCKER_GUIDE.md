# REM-CODE Lite Docker Guide 🐳

Easy setup and deployment for constitutional programming with Docker.

## Quick Start

### 1. **One-Command Setup**
```bash
# Clone and run REM-CODE Lite
git clone https://github.com/SYNOVAW/REM-CODE.git
cd REM-CODE
docker-compose up
```

### 2. **Access Constitutional Programming**
- **Web Shell**: http://localhost:8080 - Interactive constitutional programming
- **Dashboard**: http://localhost:8081 - Constitutional governance monitoring  
- **Jupyter**: http://localhost:8888 - Notebook-based constitutional development

## Docker Commands

### **Basic Usage**
```bash
# Build the container
docker build -t rem-code-lite .

# Run interactive tutorial
docker run -it rem-code-lite tutorial

# Run web shell
docker run -p 8080:8080 rem-code-lite web

# Run constitutional examples
docker run rem-code-lite examples

# Run error demo
docker run -it rem-code-lite demo
```

### **Development Setup**
```bash
# Full development environment
docker-compose up

# Run specific services
docker-compose up rem-tutorial     # Interactive tutorial
docker-compose up rem-dashboard    # Constitutional dashboard
docker-compose up rem-jupyter      # Jupyter notebooks

# Run with profiles
docker-compose --profile tutorial up      # Tutorial mode
docker-compose --profile dashboard up     # Dashboard mode  
docker-compose --profile jupyter up       # Jupyter mode
```

### **Production Deployment**
```bash
# Production mode
docker-compose -f docker-compose.yml up -d

# Scale services
docker-compose up --scale rem-code-lite=3

# Update to latest
docker-compose pull && docker-compose up -d
```

## Service Descriptions

### **rem-code-lite** (Main Service)
- **Purpose**: Primary constitutional programming interface
- **Port**: 8080
- **Features**: Web-based REM-CODE shell, constitutional validation
- **Volume**: Persistent user programs and data

### **rem-tutorial** (Interactive Learning)
- **Purpose**: Step-by-step constitutional programming tutorial
- **Mode**: Interactive CLI
- **Features**: 6 comprehensive lessons, hands-on exercises

### **rem-dashboard** (Monitoring)
- **Purpose**: Constitutional governance monitoring and analytics
- **Port**: 8081
- **Features**: Real-time validation metrics, signature tracking

### **rem-jupyter** (Development)
- **Purpose**: Notebook-based constitutional programming
- **Port**: 8888
- **Features**: Interactive development, educational notebooks

## Volume Mounts

### **Persistent Data**
```bash
./user_programs -> /app/user_programs  # Your constitutional programs
./data -> /app/data                    # Application data
./logs -> /app/logs                    # System logs
./examples -> /app/examples            # Tutorial examples (read-only)
```

### **Custom Mounting**
```bash
# Mount custom directory
docker run -v /your/programs:/app/user_programs rem-code-lite

# Mount configuration
docker run -v /your/config.json:/app/config.json rem-code-lite
```

## Environment Variables

### **Configuration**
```bash
REM_CODE_MODE=development      # development, production, tutorial, dashboard
PORT=8080                      # Service port
REM_CODE_VERSION=2.4.0        # Version identifier
```

### **Example Usage**
```bash
# Custom port and mode
docker run -p 9000:9000 -e PORT=9000 -e REM_CODE_MODE=production rem-code-lite web

# Tutorial mode
docker run -e REM_CODE_MODE=tutorial rem-code-lite tutorial
```

## Docker Compose Profiles

### **Available Profiles**
- `tutorial` - Interactive constitutional programming tutorial
- `dashboard` - Constitutional governance monitoring
- `jupyter` - Notebook-based development environment

### **Profile Usage**
```bash
# Run tutorial only
docker-compose --profile tutorial up

# Run dashboard and jupyter
docker-compose --profile dashboard --profile jupyter up

# Run everything
docker-compose --profile tutorial --profile dashboard --profile jupyter up
```

## Health Checks

### **Container Health**
```bash
# Check container health
docker ps
docker inspect rem-code-lite | grep Health

# View health logs
docker logs rem-code-lite
```

### **Service Health Endpoints**
- **Web Shell**: http://localhost:8080/health
- **Dashboard**: http://localhost:8081/health
- **Jupyter**: http://localhost:8888/ (token required)

## Data Persistence

### **Important Directories**
```bash
user_programs/     # Your constitutional programs (PERSISTENT)
data/             # Application data and exports (PERSISTENT)  
logs/             # System and error logs (PERSISTENT)
examples/         # Tutorial examples (READ-ONLY)
```

### **Backup Strategy**
```bash
# Backup user data
docker run --rm -v rem-code_user_programs:/data alpine tar czf - /data > backup.tar.gz

# Restore user data
docker run --rm -v rem-code_user_programs:/data alpine tar xzf - < backup.tar.gz
```

## Troubleshooting

### **Common Issues**

**Port conflicts:**
```bash
# Check port usage
netstat -tulpn | grep :8080

# Use different ports
docker run -p 9080:8080 rem-code-lite web
```

**Permission issues:**
```bash
# Fix volume permissions
sudo chown -R 1000:1000 ./user_programs ./data ./logs
```

**Container won't start:**
```bash
# Check logs
docker logs rem-code-lite

# Debug mode
docker run -it rem-code-lite /bin/bash
```

### **Debug Mode**
```bash
# Interactive shell access
docker exec -it rem-code-lite /bin/bash

# Check constitutional framework
docker exec rem-code-lite python -c "import constitutional; print('OK')"

# Run diagnostics
docker exec rem-code-lite python constitutional/error_demo.py
```

## Performance Optimization

### **Resource Limits**
```bash
# Limit memory and CPU
docker run --memory=1g --cpus=2 rem-code-lite

# Production limits in compose
services:
  rem-code-lite:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2'
```

### **Caching**
```bash
# Multi-stage build for smaller images
docker build --target production .

# Use build cache
docker build --cache-from rem-code-lite .
```

## Security

### **Container Security**
- Runs as non-root user `remcode`
- Read-only examples directory
- Health checks for monitoring
- No unnecessary system packages

### **Network Security**
```bash
# Custom network
docker network create rem-code-secure
docker run --network rem-code-secure rem-code-lite

# Firewall rules
sudo ufw allow 8080/tcp  # Web shell
sudo ufw allow 8081/tcp  # Dashboard
```

## Advanced Usage

### **Custom Entrypoints**
```bash
# Run specific command
docker run rem-code-lite python your_script.py

# Interactive Python
docker run -it rem-code-lite python

# Custom shell
docker run -it rem-code-lite /bin/bash
```

### **Development Override**
```bash
# Override compose for development
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```

### **Multi-Stage Deployment**
```bash
# Build for different environments
docker build --target development -t rem-code-lite:dev .
docker build --target production -t rem-code-lite:prod .
```

## Integration Examples

### **CI/CD Pipeline**
```yaml
# .github/workflows/docker.yml
- name: Build and test
  run: |
    docker build -t rem-code-lite:test .
    docker run rem-code-lite:test examples
    docker run rem-code-lite:test demo
```

### **Kubernetes Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rem-code-lite
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rem-code-lite
  template:
    spec:
      containers:
      - name: rem-code-lite
        image: rem-code-lite:2.4.0
        ports:
        - containerPort: 8080
```

## Getting Help

### **Documentation**
- See `GETTING_STARTED.md` for constitutional programming basics
- Run `docker run -it rem-code-lite tutorial` for interactive learning
- Check examples at `examples/` directory

### **Support**
- Container issues: Check logs with `docker logs rem-code-lite`
- Constitutional programming: Run error demo with `docker run -it rem-code-lite demo`
- Community: GitHub issues and discussions

---

🌀 **Ready to democratize your code with Docker?** 

Start with: `docker-compose up` and visit http://localhost:8080

*REM-CODE Lite v2.4.0 - Constitutional Programming for Everyone*