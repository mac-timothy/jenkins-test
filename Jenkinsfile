/*
=====================================================================
Jenkins Continuous Integration Pipeline
=====================================================================

Project:
    Python FastAPI Backend

Purpose:
    Automate the software testing process whenever code changes
    are pushed or Jenkins builds are triggered.

Pipeline Responsibilities:

    1. Checkout source code from Git repository.
    2. Prepare Python testing environment.
    3. Install application dependencies.
    4. Execute automated tests using pytest.
    5. Generate test reports.
    6. Publish reports inside Jenkins.
    7. Provide build status feedback.

CI Flow:

    Developer pushes code
              |
              v
        Jenkins starts build
              |
              v
        Checkout source
              |
              v
        Create Python environment
              |
              v
        Install dependencies
              |
              v
        Run automated tests
              |
              v
        Publish test reports
              |
              v
        Build SUCCESS / FAILURE


=====================================================================
*/


pipeline {


    /*
    ================================================================
    Jenkins Agent

    Defines where this pipeline will execute.

    ================================================================
    */

    agent any



    /*
    ================================================================
    Pipeline Options

    Prevent Jenkins from automatically checking out code twice.

    Checkout is handled manually using:

        checkout scm

    ================================================================
    */

    options {

        skipDefaultCheckout(true)

    }




    /*
    ================================================================
    Environment Configuration

    Jenkins test environment.

    This tells the application to load:

        .env.test

    instead of:

        .env

    ================================================================
    */

    environment {

    ENVIRONMENT = "test"

    TEST_DB_USER = credentials('test-db-user')
    TEST_DB_PASSWORD = credentials('test-db-password')
    TEST_DB_HOST = credentials('test-db-host')
    TEST_DB_PORT = credentials('test-db-port')
    TEST_DB_NAME = credentials('test-db-name')

}





    stages {



        /*
        ============================================================
        Stage 1: Checkout Source Code
        ============================================================
        */

        stage('Checkout Source') {


            steps {


                echo 'Checking out source code from Git repository...'



                /*
                checkout scm

                Jenkins uses configured:

                    - Repository URL
                    - Credentials
                    - Branch

                */

                checkout scm


            }

        }






        /*
        ============================================================
        Stage 2: Install Dependencies

        Purpose:

            Create Python environment and install packages.

        Creates:

            backend/venv

        Installs:

            requirements.txt
            pytest
            pytest-html

        ============================================================
        */


        stage('Install Dependencies') {


            steps {


                echo 'Creating Python environment and installing dependencies...'



                sh '''

                set -e


                cd backend



                echo "Checking Python version..."

                python3 --version



                echo "Creating virtual environment..."

                if [ ! -d "venv" ]; then

                    python3 -m venv venv

                fi



                echo "Activating virtual environment..."

                . venv/bin/activate



                echo "Upgrading pip..."

                pip install --upgrade pip



                echo "Installing application dependencies..."

                pip install -r requirements.txt



                echo "Installing testing tools..."

                pip install pytest pytest-cov pytest-html



                echo "Dependencies installed successfully."


                '''

            }

        }







        /*
        ============================================================
        Stage 3: Run Automated Tests


        Purpose:

            Execute automated tests using pytest.


        Reports generated:


            test-results.xml

                Jenkins JUnit report


            test-report.html

                Browser HTML report


        ============================================================
        */


        stage('Run Automated Tests') {


            steps {


                echo 'Running automated pytest test suite...'



                sh '''

                set -e



                cd backend



                echo "Activating virtual environment..."

                . venv/bin/activate




                echo "================================"

                echo "Environment Information"

                echo "================================"



                echo "ENVIRONMENT=$ENVIRONMENT"




                echo "================================"

                echo "Checking backend files"

                echo "================================"



                ls -la




                echo "================================"

                echo "Checking environment files"

                echo "================================"



                ls -la .env* || true





                echo "================================"

                echo "Executing pytest"

                echo "================================"


             pytest --junitxml=test-results.xml --html=test-report.html --self-contained-html


                '''

            }

        }







        /*
        ============================================================
        Stage 4: Publish Test Reports


        Jenkins displays:

            - Passed tests
            - Failed tests
            - Error details


        ============================================================
        */


        stage('Publish Reports') {


            steps {


                echo 'Publishing test reports to Jenkins dashboard...'



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






                /*
                Keep reports attached to Jenkins build.

                */

                archiveArtifacts(

                    artifacts: 'backend/test-report.html, backend/test-results.xml',

                    allowEmptyArchive: true

                )


            }

        }


    }








    /*
    ================================================================
    Post Build Actions

    Executes after pipeline completion.

    ================================================================
    */


    post {



        success {


            echo 'BUILD SUCCESS - All automated tests passed.'


        }




        failure {


            echo 'BUILD FAILED - Review console output and test reports.'


        }





        always {


            echo 'Pipeline execution completed.'


        }


    }


}