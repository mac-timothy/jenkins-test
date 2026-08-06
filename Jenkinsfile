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

    "any" means Jenkins can run this job on any available worker node.

    In our case:
        Jenkins Docker container

    ================================================================
    */

    agent any




    /*
    ================================================================
    Environment Configuration

    Environment variables are available to all pipeline stages.

    The application database configuration checks:

        ENVIRONMENT=test


    When this value exists:

        database.py

    loads:

        .env.test


    instead of:

        .env


    This ensures Jenkins tests use the testing database
    and never touch production data.


    Later, database credentials will be moved into Jenkins
    Credentials Manager instead of files.

    ================================================================
    */


    environment {


        ENVIRONMENT = "test"


    }





    stages {



        /*
        ============================================================
        Stage 1: Checkout Source Code

        Purpose:

            Download the latest source code from GitHub.


        Jenkins performs:

            Git clone / Git fetch
                    |
                    v
            Checkout selected branch


        Example:

            mac branch


        ============================================================
        */


        stage('Checkout Source') {


            steps {


                echo 'Checking out source code from Git repository...'



                /*
                checkout scm

                Uses the Git repository configured
                inside the Jenkins pipeline job.

                Jenkins automatically knows:

                    - repository URL
                    - credentials
                    - branch

                */


                checkout scm


            }

        }







        /*
        ============================================================
        Stage 2: Install Dependencies


        Purpose:

            Prepare a clean Python environment.


        Jenkins containers are temporary environments.

        They do not contain:

            - project packages
            - virtual environments
            - pytest


        This stage creates:

            backend/venv


        Then installs:

            requirements.txt


        ============================================================
        */


        stage('Install Dependencies') {


            steps {


                echo 'Creating Python environment and installing dependencies...'



                sh '''


                # Move into backend application folder

                cd backend



                # Create isolated Python environment

                python3 -m venv venv



                # Activate virtual environment

                . venv/bin/activate



                # Upgrade package manager

                pip install --upgrade pip



                # Install application dependencies

                pip install -r requirements.txt



                # Install testing tools

                pip install pytest pytest-cov pytest-html



                '''


            }

        }








        /*
        ============================================================
        Stage 3: Run Automated Tests


        Purpose:

            Execute the application's automated tests.


        Testing framework:

            pytest


        Generated reports:


            test-results.xml

                Used by Jenkins to display test results.


            test-report.html

                Human-friendly HTML test report.


        Build behaviour:


            Test passes:

                Pipeline continues.


            Test fails:

                Pipeline stops and build fails.


        ============================================================
        */


        stage('Run Automated Tests') {


            steps {


                echo 'Running automated pytest test suite...'



                sh '''



                # Enter backend directory

                cd backend



                # Activate Python environment

                . venv/bin/activate



                # Execute tests

                pytest \\
                --junitxml=test-results.xml \\
                --html=test-report.html \\
                --self-contained-html



                '''


            }

        }









        /*
        ============================================================
        Stage 4: Publish Test Reports


        Purpose:


            Display test information inside Jenkins.


        Jenkins will show:


            - Number of tests executed
            - Passed tests
            - Failed tests
            - Error details


        Reports:

            JUnit XML
                Jenkins native test reporting


            HTML Report
                Detailed browser report


        ============================================================
        */


        stage('Publish Reports') {


            steps {


                echo 'Publishing test reports to Jenkins dashboard...'



                /*
                Publish JUnit test results

                Jenkins understands XML format
                and creates the Test Result dashboard.

                */


                junit(


                    testResults: 'backend/test-results.xml',


                    allowEmptyResults: true


                )






                /*
                Publish HTML report


                Creates a link in Jenkins:

                    Pytest HTML Report


                Developers can open it
                and inspect failures.

                */


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








    /*
    ================================================================
    Post Build Actions


    Runs after the pipeline finishes.

    Jenkins executes these blocks depending
    on the final build result.


    ================================================================
    */


    post {



        /*
        Runs when every test passes.

        */


        success {


            echo 'BUILD SUCCESS - All automated tests passed.'


        }




        /*
        Runs when something fails.

        Possible causes:

            - dependency installation failure
            - test failure
            - application error


        */


        failure {


            echo 'BUILD FAILED - Review console output and test reports.'


        }





        /*
        Always executes regardless of result.

        Useful for:

            - cleanup
            - notifications
            - logging

        */


        always {


            echo 'Pipeline execution completed.'


        }


    }


}