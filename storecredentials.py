from flask import Flask, render_template, request, redirect
import requests
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    API_ENDPOINT = os.environ.get('API_ENDPOINT')
    if not API_ENDPOINT:
        return "API endpoint URL not found in environment variables."
    if request.method == 'POST':
        # Handle the form submission
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # JSON payload containing the registration data
        registration_data = {
            'email': email,
            'username': username,
            'password': password
        }
        try:
            print("endpoint url for api is", f'https://{API_ENDPOINT}.execute-api.us-east-1.amazonaws.com/prod/registration')
            # Make a POST request to the API endpoint
            response = requests.post(f'https://{API_ENDPOINT}.execute-api.us-east-1.amazonaws.com/prod/registration', json=registration_data)

            # Check the response status code
            if response.status_code == 200:
                # Registration successful, render the login page
                return render_template('login.html')
            else:
                # Registration failed, show an error message
                return "Registration failed. Please try again later."

        except requests.exceptions.RequestException as e:
            return "An error occurred. Please try again later."

    # If it's a GET request or the form submission is unsuccessful, render the registration page
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # API_ENDPOINT = "https://tyd2qq7nwa.execute-api.us-east-1.amazonaws.com/dev/login"
    API_ENDPOINT = os.environ.get('API_ENDPOINT')
    if not API_ENDPOINT:
        return "API endpoint URL not found in environment variables."
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']

        # JSON payload containing the username and password
        login_data = {
            'username': username,
            'password': password
        }

        try:
            # Make a POST request to the API endpoint
            response = requests.post(f'https://{API_ENDPOINT}.execute-api.us-east-1.amazonaws.com/prod/login', json=login_data)

            # Check the response status code
            if response.status_code == 200:
                # Request was successful, redirect to the '/upload' page
                return redirect('/upload')
            else:
                # Request failed, show the error message
                return "Login failed. Invalid email or password."

        except requests.exceptions.RequestException as e:
            return "An error occurred. Please try again later."

    # If it's a GET request or the form submission is unsuccessful, render the login page
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if a file was submitted
        if 'file' not in request.files:
            return "No file selected."

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return "No file selected."

        # Handle the file upload
        filename = secure_filename(file.filename)
        print("uploaded image name is", filename)
        aws_access_key_id = 'ASIATRPPMZRQKLXS5UT4'
        aws_secret_access_key = 'FPhCOJIjnN/3g42/6h5chC0agzMilqAVV68DVbdR'
        aws_session_token = 'FwoGZXIvYXdzEDsaDNyNYOhjd6zGrVd7lSLHAa7Bp/pkp20qj2klq3GYXgE9C8IDwt5pd6M7O2fUe56/5lBxz575jSePV0t6H03pr5hs6KwktWsf/EjK8oXL9l4NoTi+xSy9BFVsEwfuq2bs5wzHIihK4Z3PyHBNasyLg/Euly0qXAwWR0/fJDlwgeOPEWTKCHlk/2NWg313eLqg2QDESidPr+EGYJ0Sva6V5oLcWy4tzgJqwIbZerqloPWKHzg4KkuzXkoneVUvbcsfZfvrq2rXMdJnkLWjyStIG5k0USIHFbYojtefpgYyLYNPIUl1WDTVmKdkNvL5Rbkpq5S2LXmX12ezgKtNiyteb7VmYLbTG9EK4OjPYw=='
        # Store the file in S3
        s3 = boto3.client('s3', 
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          aws_session_token=aws_session_token)
                          
        bucket_name = 'myreceiptbucket36'
        s3_key = f'{filename}'  # Customize the S3 key as needed
        print("document key is ", s3_key)
       
        try:
            s3.upload_fileobj(file, bucket_name, s3_key)
            print("File upload successful!")
            return redirect('/finalpage')
        except ClientError as e:
            print("Error:", e)
            return "File upload failed. Please try again later."
    return render_template('upload.html')
   
@app.route('/finalpage')
def final_page():
    return render_template('finalpage.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
