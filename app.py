import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
print("OAUTHLIB_INSECURE_TRANSPORT:", os.getenv('OAUTHLIB_INSECURE_TRANSPORT'))


from flask import Flask, request, jsonify, redirect, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from urllib.parse import quote as url_quote
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key for session management

# Define the scopes and the credentials file


SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read']
CLIENT_SECRETS_FILE = 'credentials.json'

def get_google_fit_service():
    """Creates a Google Fit service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        return None
    return build('fitness', 'v1', credentials=creds)


@app.route('/')
def index():
    return 'Welcome to the Fitness Data Integration Service!'

@app.route('/auth', methods=['GET'])
def authorize():
    # Initialize the OAuth flow
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Generate the authorization URL
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Handle the callback from Google's OAuth 2.0 server
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Fetch the authorization response
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Save the credentials to a file
    credentials = flow.credentials
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())

    return redirect(url_for('get_fitness_data'))

@app.route('/fitness-data', methods=['GET'])
def get_fitness_data():
    service = get_google_fit_service()
    if not service:
        return jsonify({'error': 'Authorization required.'}), 401

    # Example: Get data sources (like steps, calories burned, etc.)
    data_sources = service.users().dataSources().list(userId='me').execute()
    
    return jsonify(data_sources)

@app.route('/active-minutes', methods=['GET'])
def get_active_minutes():
    service = get_google_fit_service()
    if not service:
        return jsonify({'error': 'Authorization required.'}), 401

    # Example: Get active minutes data
    data_sources = service.users().dataSources().list(userId='me').execute()
    active_minutes_data = [source for source in data_sources.get('dataSource', [])
                           if 'active_minutes' in source.get('dataType', {}).get('name', '')]

    return jsonify(active_minutes_data)

@app.route('/active-minutes/data', methods=['GET'])
def get_active_minutes_data():
    service = get_google_fit_service()
    if not service:
        return jsonify({'error': 'Authorization required.'}), 401

    # Set the time range (e.g., last 7 days)
    end_time = int(datetime.now().timestamp() * 1000000000)  # Convert to nanoseconds
    start_time = end_time - (7 * 24 * 60 * 60 * 1000000000)  # Last 7 days

    # Specify the dataStreamId for active minutes
    data_stream_id = "derived:com.google.active_minutes:com.google.android.gms:merge_active_minutes"

    # Create the dataset ID using the start and end times
    dataset_id = f"{start_time}-{end_time}"

    # Fetch the data from the Google Fit API
    active_minutes_data = service.users().dataSources().datasets().get(
        userId='me',
        dataSourceId=data_stream_id,
        datasetId=dataset_id
    ).execute()

    return jsonify(active_minutes_data)


@app.route('/steps', methods=['GET'])
def get_steps():
    service = get_google_fit_service()
    if not service:
        return jsonify({'error': 'Authorization required.'}), 401

    # Example: Get steps data
    data_sources = service.users().dataSources().list(userId='me').execute()
    steps_data = [source for source in data_sources.get('dataSource', [])
                  if 'step_count' in source.get('dataType', {}).get('name', '')]

    return jsonify(steps_data)

@app.route('/steps/data', methods=['GET'])
def get_steps_data():
    service = get_google_fit_service()
    if not service:
        return jsonify({'error': 'Authorization required.'}), 401

    # Set the time range (last 7 days in this example)
    end_time = int(datetime.now().timestamp() * 1000000000)  # Convert to nanoseconds
    start_time = end_time - (7 * 24 * 60 * 60 * 1000000000)  # Last 7 days

    # Fetch the data for a specific dataStreamId
    # Replace with the actual dataStreamId you want to fetch data for
    data_stream_id = "derived:com.google.step_count.delta:com.google.android.gms:merge_step_deltas"

    dataset_id = f"{start_time}-{end_time}"
    steps_data = service.users().dataSources().datasets().get(
        userId='me',
        dataSourceId=data_stream_id,
        datasetId=dataset_id
    ).execute()

    return jsonify(steps_data)


@app.route('/calories', methods=['GET'])
def get_calories():
    service = get_google_fit_service()
    if not service:
        return jsonify({'error': 'Authorization required.'}), 401

    # Example: Get calories data
    data_sources = service.users().dataSources().list(userId='me').execute()
    calories_data = [source for source in data_sources.get('dataSource', [])
                     if 'calories' in source.get('dataType', {}).get('name', '')]

    return jsonify(calories_data)

@app.route('/calories/data', methods=['GET'])
def get_calories_data():
    service = get_google_fit_service()
    if not service:
        return jsonify({'error': 'Authorization required.'}), 401

    # Set the time range (e.g., last 7 days)
    end_time = int(datetime.now().timestamp() * 1000000000)  # Convert to nanoseconds
    start_time = end_time - (7 * 24 * 60 * 60 * 1000000000)  # Last 7 days

    # Specify the dataStreamId for calories expended
    data_stream_id = "derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended"

    # Create the dataset ID using the start and end times
    dataset_id = f"{start_time}-{end_time}"
    
    # Fetch the data from the Google Fit API
    calories_data = service.users().dataSources().datasets().get(
        userId='me',
        dataSourceId=data_stream_id,
        datasetId=dataset_id
    ).execute()

    return jsonify(calories_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

