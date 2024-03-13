# start app
start-app-dev:
	uvicorn src.main:app --reload

start-app-tracer:
	opentelemetry-instrument uvicorn src.main:app --reload

start-app-docker:
	docker build --tag "jigglediggle1/image-captioning" .
	docker run -d --name="image-captioning" -p 30000:30000 "jigglediggle1/image-captioning"

# run jenkins if not exists
run-jenkins:
	docker build --tag "jigglediggle1/jenkins" jenkins/.
	docker run -d --name="jenkins" -p 8085:8080 "jigglediggle1/jenkins"

start-jenkins-compose:
	docker compose -f ./jenkins/docker-compose.yaml up -d

stop-jenkins-compose:
	docker compose -f ./jenkins/docker-compose.yaml stop

start-monitoring-compose:
	docker compose -f ./monitoring/docker-compose.yaml up -d

stop-monitoring-compose:
	docker compose -f ./monitoring/docker-compose.yaml stop