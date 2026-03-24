pipeline {

    agent any

    environment {
        APP_NAME = "currency-converter"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code from Git..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                sh 'python3 --version'
                sh 'pip3 install -r requirements.txt --break-system-packages'
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests with pytest..."
                sh 'python3 -m pytest test_converter.py -v --tb=short'
            }
        }

        stage('Deploy') {
            steps {
                echo "All tests passed!"
                echo "App: currency-converter deployed successfully on bare Python"
                sh 'ls -la converter.py'
                sh 'echo "Deployment complete"'
            }
        }
    }

    post {
        success {
            echo "Pipeline PASSED — currency-converter is live!"
        }
        failure {
            echo "Pipeline FAILED — check the logs above."
        }
        always {
            echo "Pipeline finished."
        }
    }
}