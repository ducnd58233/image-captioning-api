pipeline {
    agent any

    options{
        // Max number of build logs to keep and days to keep
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        // Enable timestamp at each job in the pipeline
        timestamps()
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                echo 'Building successful!'
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