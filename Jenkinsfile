pipeline {


    agent any



    stages {


        // =================================================
        // Stage 1:
        // Get source code from GitHub
        //
        // Jenkins automatically checks out the repository
        // that is configured in the pipeline job.
        //
        // =================================================

        stage('Checkout') {


            steps {


                echo 'Checking out source code...'


                checkout scm


            }

        }





        // =================================================
        // Stage 2:
        // Install Python dependencies
        //
        // Jenkins machines are clean environments.
        //
        // Therefore we install:
        //
        // - Application dependencies
        // - Testing tools
        //
        // =================================================

        stage('Install Dependencies') {


            steps {


                echo 'Installing Python dependencies...'


                sh '''

                cd backend


                python3 -m venv venv || true


                . venv/bin/activate


                pip install --upgrade pip


                pip install -r requirements.txt


                pip install pytest pytest-cov pytest-html


                '''


            }

        }





        // =================================================
        // Stage 3:
        // Run automated tests
        //
        // This is the most important CI stage.
        //
        // If tests fail:
        //
        // Jenkins build becomes FAILED
        //
        // =================================================

        stage('Run Tests') {


            steps {


                echo 'Running automated tests...'


                sh '''

                cd backend


                . venv/bin/activate



                pytest \
                --junitxml=test-results.xml



                '''


            }

        }


    }





    // =====================================================
    // Post actions
    //
    // These execute after the pipeline finishes.
    //
    // =====================================================

    post {


        always {


            echo 'Publishing test reports...'



            // Jenkins reads this file
            // and displays test results.

            junit(

                testResults: 'backend/test-results.xml',

                allowEmptyResults: true

            )



            // Publish pytest HTML report

            publishHTML([

                allowMissing: true,

                alwaysLinkToLastBuild: true,

                keepAll: true,

                reportDir: 'backend',

                reportFiles: 'test-report.html',

                reportName: 'Pytest HTML Report'

            ])



        }





        success {


            echo 'BUILD SUCCESS - All tests passed'


        }





        failure {


            echo 'BUILD FAILED - Tests failed'


        }


    }

}