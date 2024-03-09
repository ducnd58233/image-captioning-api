# start app
start-app-dev:
	uvicorn src.main:app --reload

# run jenkins
run-jenkins:
	docker build --tag "jenkins" jenkins/.
	docker run -d --name="jenkins" -p 8085:8080 "jenkins"