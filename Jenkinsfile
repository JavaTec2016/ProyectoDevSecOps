pipeline{
    agent any

  tools { nodejs 'node26' }
  options {
    timestamps()
    disableConcurrentBuilds()
  }
  stages{
    stage('Notify start') {
      steps {
        slackSend(color: '#439FE0',
                  message: "Iniciando: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|open>)")
      }
    }
    stage('Backend tests') {
      environment {
        DB_HOST = 'jenkins_db'
        DB_NAME = 'db_colectas_2026'
        DB_USER = 'dominik'
        DB_PASSWORD = 'santiago'
      }
      steps {
        dir('backend') {
          sh '''
            python3 -m venv .venv
            . .venv/bin/activate
            pip install -r requirements.txt
            python manage.py test
          '''
        }
      }
    }
    stage('Frontend tests') {
      steps {
        dir('frontend') {
          sh 'npm ci' //no hay script de pruebas
        }
      }
    }
    stage('SonarQube analysis') {
      steps {
        script { scannerHome = tool 'sonarqube_scanner' }
        withSonarQubeEnv('sonarqube') {
          sh "${scannerHome}/bin/sonar-scanner"
        }
      }
    }
    stage('Build parts') {
      steps {
        dir('frontend') { sh 'npm run build' }
        dir('backend') {
          sh '. .venv/bin/activate && python manage.py check'
        }
      }
    }
    stage('Mergear test') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'github_jenkins',
                         usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
          sh '''
            git config user.name  "Jenkins"
            git config user.email "jenkins@local"

            git fetch origin main:refs/remotes/origin/main
            git checkout -B main origin/main
            git merge --no-ff ${GIT_COMMIT} -m "Merge test into main (build ${BUILD_NUMBER})"

            git push "https://${GIT_USER}:${GIT_TOKEN}@${GIT_URL#https://}" main
          '''
        }
        slackSend(color: 'good',
                  message: "Merged `test` into `main` (${env.GIT_COMMIT.take(7)}) after build #${env.BUILD_NUMBER}")
      }
    }
  }
  //despues de buildear
  post {
    success {
      slackSend(color: 'good',
                message: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|open>)")
    }
    failure {
      slackSend(color: 'danger',
                message: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}console|console log>)")
      sh 'git merge --abort || true'
    }
    unstable {
      slackSend(color: 'warning',
                message: "UNSTABLE: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|open>)")
    }
    aborted {
      slackSend(color: 'warning',
                message: "ABORTED: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
    }
  }
}
