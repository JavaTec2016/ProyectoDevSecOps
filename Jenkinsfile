pipeline{
    agent any

  tools { nodejs 'node26' }
  options {
    timestamps()
    disableConcurrentBuilds()
  }
  stages{
    stage('Backend tests') {
      steps {
        sh '''
          docker compose -f compose.yaml up -d db
          docker compose -f compose.yaml run -d api
        '''
      }
    }
    stage('Frontend tests') {
      steps {
        dir('frontend') {
          sh 'npm ci'
          sh 'npm run dev'
        }
      }
    }
    stage('SonarQube analysis') {
      steps {
        script { scannerHome = tool 'SonarScanner' }
        withSonarQubeEnv('sonarqube') {
          sh "${scannerHome}/bin/sonar-scanner"
        }
      }
    }
    stage('Build images') {
      steps {
        sh 'docker compose build'
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
