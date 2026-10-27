pipeline{
    agent any

  tools { nodejs 'node26' }
  options {
    timestamps()
    disableConcurrentBuilds()
  }
  stages{
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

            git push https://${GIT_USER}:${GIT_TOKEN}@github.com/ProyectoDevSecOps.git main
          '''
        }
      }
    }
  }
}
