import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


# Zendesk subdomain (replace with yours)
subdomain = ""

# Your Zendesk email and API token
email = ""  # Replace with your email
api_token = ""  # Replace with your API token

# Zendesk API endpoint to fetch tickets
url = f"https://{subdomain}.zendesk.com/api/v2/tickets.json"

# Make the request with basic authentication (email/token)
response = requests.get(url, auth=HTTPBasicAuth(f"{email}/token", api_token))

# auth_string = f"{email}/token:{api_token}"
# auth_bytes = auth_string.encode("utf-8")
# auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

# # Set the Authorization header
# headers = {
#     "Authorization": f"Basic {auth_base64}"
# }

# # Make the request
# response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    tickets = response.json()['tickets']  # Extract the tickets from the JSON response
    df = pd.DataFrame(tickets)

    # Select relevant columns for insights
    df = df[['id', 'subject', 'status', 'created_at', 'updated_at', 'priority', 'type']]

    print("Ticket DataFrame:\n", df.head())
    # Count the number of tickets by status
    status_distribution = df['status'].value_counts()
    print("Ticket Status Distribution:\n", status_distribution)
    # Convert created_at column to datetime
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Group by the date and count the number of tickets created per day
    tickets_per_day = df.groupby(df['created_at'].dt.date).size()
    print("Tickets Created Per Day:\n", tickets_per_day)

        # Count the number of tickets by priority
    priority_distribution = df['priority'].value_counts()
    print("Ticket Priority Distribution:\n", priority_distribution)
    # Example: Calculate ticket age (difference between created_at and updated_at)
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    df['ticket_age'] = df['updated_at'] - df['created_at']
    print("Ticket Age:\n", df[['id', 'subject', 'ticket_age']].head())

    # Plot the status distribution
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x='status')
    plt.title('Ticket Status Distribution')
    plt.show()


else:
    print(f"Failed to fetch tickets. Status Code: {response.status_code}")
