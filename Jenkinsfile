pipeline {
    environment {
        imagename = "nepiskopos/appimg"
        dockerImage = ''
        containerName = 'appcont'
    }

    agent any

    stages {
        stage('Cloning Git') {
            steps {
                git([url: 'https://github.com/nepiskopos/predict-missing-positive-word.git', branch: 'main'])
            }
        }

        stage('Building image') {
            steps {
                script {
                    dockerImage = docker.build "${imagename}:latest"
                }
            }
        }

        stage('Running image') {
            steps {
                script {
                    sh "docker run -d -p 8888:8000 --name ${containerName} ${imagename}:latest"
                    sh "sleep 2"
                    sh "curl -X 'POST' 'http://0.0.0.0:8888/predict' -H 'accept: application/json' -H 'Content-Type: text/plain' -d 'I wish you have a <blank> day!'"
                    // Perform any additional steps needed while the container is running
                }
            }
        }

        stage('Stop and Remove Container') {
            steps {
                script {
                    sh "docker stop ${containerName} || true"
                    sh "docker rm ${containerName} || true"
                }
            }
        }
    }
}
