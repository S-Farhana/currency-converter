// Jenkinsfile (without Docker)
pipeline {
    agent any   // Run on any available Jenkins agent

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest test_converter.py -v'
            }
        }

        stage('Run App') {
            steps {
                sh 'python converter.py'
            }
        }
    }

    post {
        success { echo 'Pipeline passed! App is working.' }
        failure { echo 'Something failed. Check the logs.' }
    }
}