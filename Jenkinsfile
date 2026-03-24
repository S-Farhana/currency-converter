// ─────────────────────────────────────────────────────────
// Jenkinsfile (WITHOUT Docker)
// CI/CD Pipeline for Currency Converter
//
// How to use:
//   1. Create a new Pipeline job in Jenkins
//   2. Point it to your GitHub repo
//   3. Jenkins finds this file and runs it automatically
// ─────────────────────────────────────────────────────────

pipeline {

    // "agent any" = run on whichever Jenkins agent is free
    agent any

    // Environment variables available to all stages
    environment {
        APP_NAME = "currency-converter"
    }

    stages {

        // ── Stage 1: Get the code ──────────────────────────
        stage('Checkout') {
            steps {
                echo "Checking out source code from Git..."
                // Jenkins automatically checks out your repo
                // when connected via SCM — this is just a label
                checkout scm
            }
        }

        // ── Stage 2: Set up Python environment ────────────
        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                sh '''
                    python3 --version
                    pip3 install -r requirements.txt
                '''
            }
        }

        // ── Stage 3: Run tests (THE CI PART) ──────────────
        stage('Run Tests') {
            steps {
                echo "Running unit tests with pytest..."
                sh '''
                    python3 -m pytest test_converter.py -v --tb=short
                '''
            }
            // If tests fail, the pipeline stops here.
            // Nothing broken ever reaches the next stage.
        }

        // ── Stage 4: Run the app (THE CD PART) ────────────
        stage('Deploy') {
            steps {
                echo "Tests passed! Running the application..."
                sh 'echo "App: ${APP_NAME} deployed successfully on bare Python"'
                // In a real project: copy to server, restart service, etc.
                // For demo: just confirm the app can be invoked
                sh 'python3 -c "from converter import convert_currency; print(\"App import OK\")"'
            }
        }
    }

    // ── Post-pipeline actions ──────────────────────────────
    post {
        success {
            echo "✅ Pipeline PASSED — ${env.APP_NAME} is live!"
        }
        failure {
            echo "❌ Pipeline FAILED — check the logs above."
        }
        always {
            echo "Pipeline finished. Branch: ${env.BRANCH_NAME ?: 'main'}"
        }
    }
}