Deployment Guide
==============

This guide provides comprehensive information about deploying the AI-powered project in various environments.

Deployment Options
----------------

Local Development
~~~~~~~~~~~~~~~

1. Set up the development environment:

   .. code-block:: bash

      # Create and activate virtual environment
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

      # Install dependencies
      pip install -e ".[dev]"

      # Set up environment variables
      cp .env.example .env
      # Edit .env with your configuration

2. Run the development server:

   .. code-block:: bash

      # Start the development server
      uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

Docker Deployment
~~~~~~~~~~~~~~~

1. Create a Dockerfile:

   .. code-block:: dockerfile

      # Use Python 3.11 slim image
      FROM python:3.11-slim

      # Set working directory
      WORKDIR /app

      # Install system dependencies
      RUN apt-get update && apt-get install -y \
          build-essential \
          && rm -rf /var/lib/apt/lists/*

      # Copy requirements
      COPY pyproject.toml .

      # Install dependencies
      RUN pip install --no-cache-dir .

      # Copy application code
      COPY . .

      # Set environment variables
      ENV PYTHONPATH=/app
      ENV PYTHONUNBUFFERED=1

      # Expose port
      EXPOSE 8000

      # Run the application
      CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

2. Create docker-compose.yml:

   .. code-block:: yaml

      version: '3.8'

      services:
        app:
          build: .
          ports:
            - "8000:8000"
          environment:
            - POSTGRES_SERVER=db
            - REDIS_HOST=redis
          depends_on:
            - db
            - redis
          volumes:
            - .:/app
          healthcheck:
            test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
            interval: 30s
            timeout: 10s
            retries: 3

        db:
          image: postgres:15
          environment:
            - POSTGRES_USER=${POSTGRES_USER}
            - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
            - POSTGRES_DB=${POSTGRES_DB}
          volumes:
            - postgres_data:/var/lib/postgresql/data
          healthcheck:
            test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
            interval: 10s
            timeout: 5s
            retries: 5

        redis:
          image: redis:7
          command: redis-server --requirepass ${REDIS_PASSWORD}
          volumes:
            - redis_data:/data
          healthcheck:
            test: ["CMD", "redis-cli", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5

      volumes:
        postgres_data:
        redis_data:

3. Build and run with Docker Compose:

   .. code-block:: bash

      # Build and start services
      docker-compose up --build

      # Stop services
      docker-compose down

Kubernetes Deployment
~~~~~~~~~~~~~~~~~~

1. Create deployment configuration:

   .. code-block:: yaml

      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: ai-app
      spec:
        replicas: 3
        selector:
          matchLabels:
            app: ai-app
        template:
          metadata:
            labels:
              app: ai-app
          spec:
            containers:
            - name: ai-app
              image: your-registry/ai-app:latest
              ports:
              - containerPort: 8000
              env:
              - name: POSTGRES_SERVER
                valueFrom:
                  configMapKeyRef:
                    name: ai-app-config
                    key: postgres-server
              - name: REDIS_HOST
                valueFrom:
                  configMapKeyRef:
                    name: ai-app-config
                    key: redis-host
              resources:
                requests:
                  memory: "512Mi"
                  cpu: "250m"
                limits:
                  memory: "1Gi"
                  cpu: "500m"
              livenessProbe:
                httpGet:
                  path: /health
                  port: 8000
                initialDelaySeconds: 5
                periodSeconds: 10
              readinessProbe:
                httpGet:
                  path: /health
                  port: 8000
                initialDelaySeconds: 5
                periodSeconds: 10

2. Create service configuration:

   .. code-block:: yaml

      apiVersion: v1
      kind: Service
      metadata:
        name: ai-app-service
      spec:
        selector:
          app: ai-app
        ports:
        - port: 80
          targetPort: 8000
        type: LoadBalancer

3. Create ConfigMap:

   .. code-block:: yaml

      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: ai-app-config
      data:
        postgres-server: "db-service"
        redis-host: "redis-service"
        log-level: "INFO"

4. Create Secrets:

   .. code-block:: yaml

      apiVersion: v1
      kind: Secret
      metadata:
        name: ai-app-secrets
      type: Opaque
      data:
        secret-key: <base64-encoded-secret>
        openai-api-key: <base64-encoded-key>
        anthropic-api-key: <base64-encoded-key>

5. Deploy to Kubernetes:

   .. code-block:: bash

      # Apply configurations
      kubectl apply -f k8s/

      # Check deployment status
      kubectl get deployments
      kubectl get pods
      kubectl get services

Cloud Deployment
~~~~~~~~~~~~~~

AWS Deployment
^^^^^^^^^^^^

1. Create ECR repository:

   .. code-block:: bash

      # Create repository
      aws ecr create-repository --repository-name ai-app

      # Tag and push image
      docker tag ai-app:latest $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/ai-app:latest
      aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com
      docker push $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/ai-app:latest

2. Deploy to ECS:

   .. code-block:: bash

      # Create cluster
      aws ecs create-cluster --cluster-name ai-app-cluster

      # Create task definition
      aws ecs register-task-definition --cli-input-json file://task-definition.json

      # Create service
      aws ecs create-service --cli-input-json file://service-definition.json

Google Cloud Deployment
^^^^^^^^^^^^^^^^^^^^

1. Create Container Registry:

   .. code-block:: bash

      # Configure gcloud
      gcloud config set project $PROJECT_ID

      # Tag and push image
      docker tag ai-app:latest gcr.io/$PROJECT_ID/ai-app:latest
      gcloud auth configure-docker
      docker push gcr.io/$PROJECT_ID/ai-app:latest

2. Deploy to Cloud Run:

   .. code-block:: bash

      # Deploy service
      gcloud run deploy ai-app \
        --image gcr.io/$PROJECT_ID/ai-app:latest \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated

Azure Deployment
^^^^^^^^^^^^^

1. Create Container Registry:

   .. code-block:: bash

      # Create registry
      az acr create --resource-group $RESOURCE_GROUP --name $REGISTRY_NAME --sku Basic

      # Tag and push image
      docker tag ai-app:latest $REGISTRY_NAME.azurecr.io/ai-app:latest
      az acr login --name $REGISTRY_NAME
      docker push $REGISTRY_NAME.azurecr.io/ai-app:latest

2. Deploy to App Service:

   .. code-block:: bash

      # Create App Service plan
      az appservice plan create --name $PLAN_NAME --resource-group $RESOURCE_GROUP --sku B1

      # Create Web App
      az webapp create --resource-group $RESOURCE_GROUP --plan $PLAN_NAME --name $APP_NAME

      # Deploy container
      az webapp config container set --name $APP_NAME --resource-group $RESOURCE_GROUP \
        --docker-custom-image-name $REGISTRY_NAME.azurecr.io/ai-app:latest

Monitoring and Logging
-------------------

Prometheus Metrics
~~~~~~~~~~~~~~~

1. Configure metrics endpoint:

   .. code-block:: python

      from prometheus_client import Counter, Histogram
      from prometheus_fastapi_instrumentator import Instrumentator

      # Define metrics
      request_counter = Counter(
          "http_requests_total",
          "Total HTTP requests",
          ["method", "endpoint", "status"]
      )

      request_latency = Histogram(
          "http_request_duration_seconds",
          "HTTP request duration",
          ["method", "endpoint"]
      )

      # Initialize FastAPI instrumentator
      Instrumentator().instrument(app).expose(app)

2. Access metrics:

   .. code-block:: bash

      # View metrics
      curl http://localhost:8000/metrics

Logging Configuration
~~~~~~~~~~~~~~~~~

1. Configure logging:

   .. code-block:: python

      import logging
      from logging.handlers import RotatingFileHandler

      def setup_logging():
          """Configure logging for production."""
          logger = logging.getLogger()
          logger.setLevel(logging.INFO)

          # File handler
          file_handler = RotatingFileHandler(
              "logs/app.log",
              maxBytes=10485760,  # 10MB
              backupCount=5
          )
          file_handler.setFormatter(
              logging.Formatter(
                  "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
              )
          )
          logger.addHandler(file_handler)

          # Console handler
          console_handler = logging.StreamHandler()
          console_handler.setFormatter(
              logging.Formatter(
                  "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
              )
          )
          logger.addHandler(console_handler)

Health Checks
-----------

1. Implement health check endpoint:

   .. code-block:: python

      @app.get("/health")
      async def health_check():
          """Health check endpoint."""
          try:
              # Check database connection
              await db.execute("SELECT 1")
              
              # Check Redis connection
              await redis.ping()
              
              return {
                  "status": "healthy",
                  "timestamp": time.time()
              }
          except Exception as e:
              raise HTTPException(
                  status_code=503,
                  detail=f"Service unhealthy: {str(e)}"
              )

Backup and Recovery
----------------

Database Backup
~~~~~~~~~~~~

1. Create backup script:

   .. code-block:: bash

      #!/bin/bash
      
      # Set variables
      BACKUP_DIR="/backups"
      TIMESTAMP=$(date +%Y%m%d_%H%M%S)
      
      # Create backup
      pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > \
          "$BACKUP_DIR/backup_$TIMESTAMP.sql"
      
      # Compress backup
      gzip "$BACKUP_DIR/backup_$TIMESTAMP.sql"
      
      # Clean up old backups (keep last 7 days)
      find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete

2. Schedule backups:

   .. code-block:: bash

      # Add to crontab
      0 0 * * * /path/to/backup.sh

Disaster Recovery
~~~~~~~~~~~~~~

1. Document recovery procedures:

   .. code-block:: text

      Recovery Steps:
      1. Stop all services
      2. Restore database from backup
      3. Verify data integrity
      4. Restart services
      5. Verify application functionality

2. Test recovery procedures:

   .. code-block:: bash

      # Test database restore
      gunzip -c backup_20240315_000000.sql.gz | \
          psql -h $DB_HOST -U $DB_USER -d $DB_NAME

Next Steps
---------

1. Review the :doc:`development` guide for development practices
2. Check out the :doc:`testing` guide for testing procedures
3. Explore the :doc:`../api/modules` for API documentation 