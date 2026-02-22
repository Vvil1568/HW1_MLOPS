.PHONY: start-minikube infra build deploy clean tunnel

# 0. Запуск minikube
start-minikube:
	minikube start --driver=docker --memory=4096 --cpus=4

# 1. Запуск ClearML (на хосте)
infra:
	docker compose up -d

# 2. Сборка образов (выполнять после minikube docker-env)
build:
	docker build -t backend-app:latest -f Dockerfile.backend .
	docker build -t frontend-app:latest -f Dockerfile.frontend .

# 3. Деплой в Kubernetes
deploy:
	kubectl apply -f k8s/minio.yaml
	kubectl apply -f k8s/clearml-client-config.yaml
	kubectl apply -f k8s/app-deployment.yaml
	kubectl apply -f k8s/frontend-deployment.yaml

# 4. Доступ к фронтенду
tunnel:
	minikube service frontend-service

# 5. Остановка и удаление
clean:
	kubectl delete -f k8s/ --ignore-not-found
	docker compose down
	minikube stop