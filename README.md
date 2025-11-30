# Домашнее задание 1: MLOps Service

Сервис для обучения моделей и инференса (FastAPI + gRPC + Streamlit).
Использует DVC для данных и ClearML для трекинга экспериментов.

## Требования
* Windows 10 (PowerShell)
* Docker Desktop
* Minikube

## Запуск

### 1. Подготовка окружения
Запустите Minikube и инфраструктуру ClearML (через Docker Compose на хосте):
```powershell
minikube start --driver=docker --memory=4096 --cpus=4
docker compose up -d
```
Дождитесь запуска ClearML по адресу http://localhost:8080.

### 2. Настройка ключей
1. Зайдите на http://localhost:8080.
2. В настройках профиля (Settings -> Workspace) нажмите **Create new credentials**.
3. Скопируйте `Access Key` и `Secret Key`.
4. Вставьте их в файл `k8s/app-deployment.yaml` в соответствующие поля `CLEARML_API_ACCESS_KEY` и `CLEARML_API_SECRET_KEY`.

### 3. Сборка
Соберите образы внутри окружения Minikube:
```powershell
minikube docker-env | Invoke-Expression
docker build -t backend-app:latest -f Dockerfile.backend .
docker build -t frontend-app:latest -f Dockerfile.frontend .
```

### 4. Деплой
Примените манифесты Kubernetes:
```powershell
kubectl apply -f k8s/minio.yaml
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
```

### 5. Использование
Откройте дашборд:
```powershell
minikube service frontend-service
```

1. **Datasets**: Загрузите `iris.csv` (должен быть заголовок). Это создаст бакет в MinIO и сохранит файл через DVC.
2. **Training**: Выберите модель и нажмите Train. Логи появятся в ClearML, модель сохранится в S3.
3. **Inference**: Используйте ID задачи из ClearML для предсказания.

## Структура
* `app/` - Бэкенд (FastAPI, ML, gRPC).
* `frontend/` - Дашборд Streamlit.
* `k8s/` - Конфигурация Kubernetes.
* `clearml-compose.yml` - Конфигурация ClearML Server.
* `clearml.conf` - Конфиг для авторизации ClearML в MinIO.