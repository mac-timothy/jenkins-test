"""
Authentication API Test Suite.

This file verifies authentication behaviour.

Covered scenarios:

1. Successful login
   -----------------
   A registered user should login
   using correct credentials.


2. Wrong password
   ----------------
   Existing users should not login
   with incorrect passwords.


3. Unknown user
   ----------------
   A user that does not exist
   should not authenticate.


4. Duplicate email signup
   ----------------
   The system should prevent
   creating two accounts with
   the same email.


Test flow:

pytest starts

      |
      |
conftest.py prepares database

      |
      |
test creates user

      |
      |
endpoint is tested

      |
      |
result is verified

"""





# =========================================================
# Successful login test
# =========================================================


def test_login_success(client, create_user):


    """
    Verify that a valid user
    can login successfully.


    Steps:

    1. Create a user.
    2. Login with correct password.
    3. Verify successful response.

    """



    # -----------------------------------------------------
    # Create fresh user
    #
    # Email is generated automatically
    # by create_user fixture.
    #
    # Example:
    #
    # user_12345@test.com
    #
    # -----------------------------------------------------


    user = create_user(

        username="mafabi_timothy",

        password="@Test2024"

    )





    # -----------------------------------------------------
    # Attempt login
    # -----------------------------------------------------


    response = client.post(

        "/auth/login",

        json={

            "email": user["email"],

            "password": user["password"]

        }

    )





    # -----------------------------------------------------
    # Login should succeed
    # -----------------------------------------------------


    assert response.status_code == 200, (

        f"""

        Login failed.


        Status:

        {response.status_code}


        Response:

        {response.json()}

        """

    )




    data = response.json()



    assert data["message"] == "Login successful"



    assert (

        data["user"]["email"]

        ==

        user["email"]

    )







# =========================================================
# Wrong password test
# =========================================================


def test_login_fails_with_invalid_password(
    
    client,
    
    create_user

):


    """
    Verify login fails
    when password is incorrect.


    Expected:

    HTTP 401

    """



    # Create valid account


    user = create_user(

        username="wrong_password_test",

        password="@Correct123"

    )




    # Attempt login with wrong password


    response = client.post(

        "/auth/login",

        json={

            "email": user["email"],

            "password": "WrongPassword123"

        }

    )




    assert response.status_code == 401, (

        f"""

        Invalid password was accepted.


        Status:

        {response.status_code}


        Response:

        {response.json()}

        """

    )








# =========================================================
# Unknown user login test
# =========================================================


def test_login_fails_with_unknown_user(client):


    """
    Verify unknown users
    cannot login.


    Expected:

    HTTP 401

    """



    response = client.post(

        "/auth/login",

        json={

            "email": "does_not_exist@test.com",

            "password": "Password123"

        }

    )




    assert response.status_code == 401, (

        f"""

        Unknown user was authenticated.


        Status:

        {response.status_code}


        Response:

        {response.json()}

        """

    )








# =========================================================
# Duplicate email signup test
# =========================================================


def test_signup_fails_for_existing_email(

    client,

    create_user

):


    """
    Verify duplicate emails
    cannot create multiple accounts.


    Steps:

    1. Create first user.
    2. Attempt signup again
       with same email.
    3. Expect rejection.


    Expected:

    HTTP 400

    """



    # -----------------------------------------------------
    # Create first account
    # -----------------------------------------------------


    user = create_user(

        username="mafabi timothy mac",

        password="@Test2024"

    )





    # -----------------------------------------------------
    # Try registering same email
    # -----------------------------------------------------


    response = client.post(

        "/auth/signup",

        json=user

    )






    assert response.status_code == 400, (

        f"""

        Duplicate email was allowed.


        Status:

        {response.status_code}


        Response:

        {response.json()}

        """

    )