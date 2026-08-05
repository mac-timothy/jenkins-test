pipeline {


    agent any



    stages {


        // =====================================================
        // Checkout Source Code
        //
        // Downloads the latest application code from GitHub.
        //
        // Jenkins uses the repository configured
        // in the pipeline job.
        //
        // =====================================================

        stage('Checkout Source') {


            steps {


                echo 'Checking out source code...'


                checkout scm


            }

        }





        // =====================================================
        // Setup Python Environment
        //
        // Jenkins machines are clean environments.
        //
        // This stage:
        //
        // 1. Creates Python virtual environment
        // 2. Installs project dependencies
        //
        // =====================================================

        stage('Install Dependencies') {


            steps {


                echo 'Installing Python dependencies...'


                sh '''

                cd backend


                python3 -m venv venv


                . venv/bin/activate


                pip install --upgrade pip


                pip install -r requirements.txt


                pip install pytest pytest-cov pytest-html


                '''


            }

        }





        // =====================================================
        // Execute Automated Tests
        //
        // This is the Continuous Integration step.
        //
        // If tests fail:
        //
        // Jenkins build fails.
        //
        // Reports generated:
        //
        // test-results.xml
        // test-report.html
        //
        // =====================================================

        stage('Run Automated Tests') {


            steps {


                echo 'Running pytest test suite...'


                sh '''

                cd backend


                . venv/bin/activate



                pytest \
                --junitxml=test-results.xml \
                --html=test-report.html \
                --self-contained-html


                '''


            }

        }





        // =====================================================
        // Publish Test Reports
        //
        // Displays test results inside Jenkins dashboard.
        //
        // Developers can see:
        //
        // - Passed tests
        // - Failed tests
        // - Error details
        //
        // =====================================================

        stage('Publish Reports') {


            steps {


                echo 'Publishing test reports...'


                junit(

                    testResults: 'backend/test-results.xml',

                    allowEmptyResults: true

                )



                publishHTML([

                    allowMissing: true,

                    alwaysLinkToLastBuild: true,

                    keepAll: true,

                    reportDir: 'backend',

                    reportFiles: 'test-report.html',

                    reportName: 'Pytest HTML Report'

                ])


            }

        }


    }





    // =====================================================
    // Pipeline Result Handling
    //
    // Runs after every build.
    //
    // =====================================================

    post {


        success {


            echo 'BUILD SUCCESS - All tests passed.'


        }



        failure {


            echo 'BUILD FAILED - Check test failures.'


        }



        always {


            echo 'Pipeline execution completed.'


        }


    }


}