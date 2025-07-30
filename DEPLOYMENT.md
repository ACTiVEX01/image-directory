# Deployment Guide

This guide covers various ways to deploy the Jupyter Notebook to PDF Converter.

## 🐳 Docker Deployment (Recommended)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/yourusername/jupyter-notebook-to-pdf.git
cd jupyter-notebook-to-pdf

# Build and run with Docker Compose
docker-compose up -d

# Access the application at http://localhost:5000
```

### Docker Commands

```bash
# Build the image
docker build -t jupyter-pdf-converter .

# Run the container
docker run -d \
  --name jupyter-pdf-converter \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  jupyter-pdf-converter

# View logs
docker logs jupyter-pdf-converter

# Stop the container
docker stop jupyter-pdf-converter
```

## ☁️ Cloud Deployments

### Heroku

1. **Create a Heroku app:**
   ```bash
   heroku create your-app-name
   ```

2. **Add buildpacks:**
   ```bash
   heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
   heroku buildpacks:add --index 2 heroku/python
   ```

3. **Create `Aptfile` for LaTeX:**
   ```bash
   echo "texlive-xetex
   texlive-fonts-recommended
   texlive-plain-generic
   pandoc" > Aptfile
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

### Railway

1. **Connect your GitHub repository to Railway**
2. **Add environment variables:**
   - `FLASK_ENV=production`
3. **Railway will automatically detect and deploy your app**

### DigitalOcean App Platform

1. **Create `app.yaml`:**
   ```yaml
   name: jupyter-pdf-converter
   services:
   - name: web
     source_dir: /
     github:
       repo: yourusername/jupyter-notebook-to-pdf
       branch: main
     run_command: python app.py
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     http_port: 5000
     envs:
     - key: FLASK_ENV
       value: production
   ```

### AWS ECS (Elastic Container Service)

1. **Push image to ECR:**
   ```bash
   # Create ECR repository
   aws ecr create-repository --repository-name jupyter-pdf-converter

   # Get login token
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.us-east-1.amazonaws.com

   # Tag and push
   docker tag jupyter-pdf-converter:latest <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/jupyter-pdf-converter:latest
   docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/jupyter-pdf-converter:latest
   ```

2. **Create ECS task definition and service through AWS Console**

### Google Cloud Run

1. **Build and push to Google Container Registry:**
   ```bash
   # Configure Docker to use gcloud as a credential helper
   gcloud auth configure-docker

   # Tag and push
   docker tag jupyter-pdf-converter gcr.io/your-project-id/jupyter-pdf-converter
   docker push gcr.io/your-project-id/jupyter-pdf-converter
   ```

2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy jupyter-pdf-converter \
     --image gcr.io/your-project-id/jupyter-pdf-converter \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 5000
   ```

## 🖥️ VPS/Server Deployment

### Ubuntu/Debian Server

1. **Install system dependencies:**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip python3-venv git nginx
   sudo apt install -y texlive-xetex texlive-fonts-recommended texlive-plain-generic pandoc
   ```

2. **Clone and setup the application:**
   ```bash
   git clone https://github.com/yourusername/jupyter-notebook-to-pdf.git
   cd jupyter-notebook-to-pdf
   
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create systemd service:**
   ```bash
   sudo nano /etc/systemd/system/jupyter-pdf-converter.service
   ```
   
   ```ini
   [Unit]
   Description=Jupyter PDF Converter
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/jupyter-notebook-to-pdf
   Environment=PATH=/path/to/jupyter-notebook-to-pdf/venv/bin
   ExecStart=/path/to/jupyter-notebook-to-pdf/venv/bin/python app.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

4. **Configure Nginx:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       client_max_body_size 20M;
   }
   ```

5. **Enable and start services:**
   ```bash
   sudo systemctl enable jupyter-pdf-converter
   sudo systemctl start jupyter-pdf-converter
   sudo systemctl reload nginx
   ```

### CentOS/RHEL Server

1. **Install dependencies:**
   ```bash
   sudo yum update
   sudo yum install -y python3 python3-pip git nginx
   sudo yum install -y texlive-xetex texlive-collection-fontsrecommended pandoc
   ```

2. **Follow similar steps as Ubuntu, adjusting paths as needed**

## 🔒 Production Considerations

### Security

1. **Use HTTPS:**
   ```bash
   # Install Certbot for Let's Encrypt
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

2. **Configure firewall:**
   ```bash
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   ```

3. **Environment variables:**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   ```

### Performance

1. **Use a production WSGI server (Gunicorn):**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Configure Nginx for static files and caching**

3. **Monitor resource usage and set up log rotation**

### Scaling

1. **Load balancing with multiple instances**
2. **Use Redis for session storage**
3. **Implement rate limiting**
4. **Set up monitoring and alerting**

## 📊 Monitoring

### Health Checks

The application includes a health check endpoint:
```bash
curl http://your-domain.com/
```

### Logging

Configure application logging:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Metrics

Consider integrating with:
- Prometheus + Grafana
- New Relic
- DataDog
- AWS CloudWatch

## 🔄 CI/CD Pipeline

### GitHub Actions (Already configured)

The repository includes CI/CD workflows that:
- Run tests on multiple Python versions
- Check code quality and security
- Build Docker images
- Deploy to various platforms

### Manual Deployment Script

```bash
#!/bin/bash
# deploy.sh

git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart jupyter-pdf-converter
sudo systemctl reload nginx
echo "Deployment complete!"
```

## 🐛 Troubleshooting

### Common Issues

1. **LaTeX not found:**
   - Ensure LaTeX is installed and in PATH
   - Install missing LaTeX packages

2. **Permission errors:**
   - Check file permissions for uploads/outputs directories
   - Ensure the application user has write permissions

3. **Memory issues:**
   - Monitor memory usage during large file conversions
   - Consider implementing file size limits

4. **Port conflicts:**
   - Change the port in app.py if 5000 is in use
   - Update Nginx configuration accordingly

### Logs Location

- Docker: `docker logs container-name`
- Systemd: `sudo journalctl -u jupyter-pdf-converter`
- Nginx: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`

## 📞 Support

For deployment issues:
1. Check the [troubleshooting guide](TROUBLESHOOTING.md)
2. Review application logs
3. Open an issue on GitHub with deployment details