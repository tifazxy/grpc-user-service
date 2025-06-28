pipeline {
  agent any
  environment {
    VENV = 'venv'
    PYTHON = './venv/bin/python'
    PIP = ./venv/bin/pip'
  }
  stages {
    stage('Clone') {
      steps {
        echo 'Clone Git repo...'
        
      }
    }
    stage('Setup Python') {
      steps {
        sh 'python3 -m venv ${VENV}'
        sh '${PIP} install --upgrade pip'
        sh '${PIP} install -r requirement.txt'
      }
    }
    stage('Generate Proto'){
      steps {
        sh 'make proto'
      }
    }
    stage('Run Tests'){
      steps {
        echo 'Placeholder until we have tests :D'
      }
    }
  }
  post {
    always {
      echo 'Pipeline completed.'
    }
    success {
      echo 'Success!'
    }
    failure {
      echo 'Failed'
    }
  }
}
