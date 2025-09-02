
# 🚀 AI-Powered Feedback Analyzer with Flask, SQL & Transformers  

This project integrates **Flask**, **SQL**, and **AI (HuggingFace Transformers)** inside a **Docker & Kubernetes** environment.  
It demonstrates how DevOps practices can be applied to deploy an AI + Database app at scale.  

---

## ✨ Features
- 📊 SQL Integration → Store & query user feedback  
- 🤖 AI Sentiment Analysis → NLP with HuggingFace  
- 🐳 Dockerized → Containerized for portability  
- ☸️ Kubernetes → Deployment with ClusterIP, ConfigMaps, Secrets & HPA  
- 🌐 Ingress → Expose the app externally  

---

## 📂 Project Structure
- `app/` → Flask app & ML code  
- `docker/` → Dockerfile  
- `k8s-manifests/` → Kubernetes YAMLs (deployment, service, ingress, hpa, configmap, secret)  
- `docs/` → Screenshots & sample outputs  

---

## ⚡ Tech Stack
- **Backend:** Flask (Python)  
- **Database:** SQLite / MySQL (configurable)  
- **AI Model:** HuggingFace `distilbert-base-uncased`  
- **Containerization:** Docker  
- **Orchestration:** Kubernetes  
- **Scaling:** HPA (Horizontal Pod Autoscaler)  

---

## 🐳 Run with Docker
```bash
# Build Image
docker build -t feedback-analyzer .

# Run Container
docker run -p 5000:5000 feedback-analyzer
