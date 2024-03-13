pipeline {
    agent any

    options{
        // Max number of build logs to keep and days to keep
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        // Enable timestamp at each job in the pipeline
        timestamps()
    }

    environment{
        registry = 'jigglediggle1/image-captioning'
        registryCredential = 'dockerhub'
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building...'
                    dockerImage = docker.build registry + ":$BUILD_NUMBER"
                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                    echo 'Building successful!'
                }
            }
        }

        stage('Deploy') {
            agent {
                kubernetes {
                    containerTemplate {
                        name 'helm' // Name of the container to be used for helm upgrade
                        image 'jigglediggle1/jenkins' // The image containing helm
                    }
                }
            }
            steps {
                echo 'Deploying...'
                echo 'Deploying successful!'
            }
        }
    }

   
    post {
        success {
            echo 'Pipeline succeeded! Congratulations!'
        }
        failure {
            echo 'Pipeline failed! Please check logs for details.'
        }
        always {
            echo 'Cleaning up...'
        }
    }
}