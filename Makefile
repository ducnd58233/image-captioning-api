# start app
start-app-dev:
	uvicorn src.main:app --reload

start-app-docker:
	docker build --tag "jigglediggle1/image-captioning" .
	docker run -d --name="image-captioning" -p 30000:30000 "jigglediggle1/image-captioning"

# run jenkins
run-jenkins:
	docker build --tag "jenkins" jenkins/.
	docker run -d --name="jenkins" -p 8085:8080 "jenkins"