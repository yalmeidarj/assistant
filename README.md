# LocalBot

LocalBot is a Python script that sends automated email proposals to potential clients from a CSV file using the SendGrid API. It filters out duplicate clients and sends tailored proposals based on the client category.

## Requirements

##### Python 3.6 or later

##### SendGrid Python library

##### SendGrid API key

##### CSV file containing potential clients

## Account setup

[Get your own SendGrid API Key.](https://sendgrid.com/solutions/email-api/?utm_source=bing&utm_medium=cpc&utm_term=sendgrid&utm_campaign=SendGrid_B_S_NAMER_Brand&cq_src=bing_ads&cq_cmp=SendGrid_B_S_NAMER_Brand&cq_con=SendGrid%20-%20Phrase&cq_term=sendgrid&cq_med=&cq_net=o&cq_plt=bp&msclkid=d3ad6333b626143545870706fed77301&utm_content=SendGrid%20-%20Phrase)

## Installation

Install the SendGrid Python library:

```
pip install sendgrid
```

Set up the SendGrid API key in your environment:

```
export SENDGRID_API_KEY='your_api_key_here'
```

Set up the bot email in your environment:

```
export BOT_EMAIL='your_bot_email_here'
```

### Usage

Prepare a CSV file containing potential clients with the following headers:

```
Name,Email,Category,company_name
```

Run the script:

```
python local_bot.py
```

### Example

Suppose you have a CSV file named proposals.csv with the following content:

graphql

```
Name,Email,Category,company_name
John Doe,johndoe@example.com,Plumbing Services,JD Plumbing
Jane Smith,janesmith@example.com,serviceProvider,JS Services
```

Here's a sample execution of the script:

```
python local_bot.py
```

This will send tailored email proposals to John Doe and Jane Smith based on their respective categories.

## Functions

### send_mail

Sends an email with SendGrid API.

#### Parameters

to_emails (str): A comma-separated string containing one or more email addresses of the recipient(s).
html_content (str): The HTML content of the email message.
from_email (str): The email address of the sender. Defaults to bot_email.
subject (str): The subject of the email message. Defaults to "An email scheduled by LocalBot!".
time (int): The number of seconds to wait before sending the email message. Defaults to 126 seconds (i.e., 2 minutes and 6 seconds).

#### Returns

None: This function does not return a value.
Raises
Exception: If an error occurs while sending the email, this function raises an Exception with a descriptive error message.
Example usage
python

```
send_mail('user@example.com', '<p>Hello, world!</p>')
```

### save_to_csv

Saves the client information to a CSV file.

### load_emails_from_csv

Loads email addresses from a CSV file.

### find_duplicates

Removes duplicate clients from the potential_clients list.

### send_proposals_to_clients

Sends proposals to clients based on the specified category.

#### Parameters

clients (list): A list of clients belonging to a specific category.
messages (dict): A dictionary containing the messages for each category.
category (str): The name of the category for which the proposal is being sent.

#### Returns

None: This function does not return a value.

### send_proposals

Sends proposals to potential clients by grouping them by category, removing duplicates, and sending customized proposals based on the client's category.

#### Parameters

None: This function does not take any parameters.

#### Returns

None: This function does not return a value.
