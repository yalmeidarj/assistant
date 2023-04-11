import csv
from datetime import datetime
import time
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from messages import messages, subject
import os



bot_mail = os.environ.get('BOT_EMAIL')
bot_path = os.path.abspath(__file__).replace('\\', '/').replace('local_bot.py', '')

class LocalBot:
    def __init__(self, local_path=bot_path):
        self.local_path = local_path    
    def send_mail(self, to_emails:str, html_content, from_email:str=bot_mail, subject:str="An email scheduled by LocalBot!", time:int=126):
        """
        # Send an email with SendGrid API.

        ## Parameters:
        - to_emails (str): A comma-separated string containing one or more email addresses of the recipient(s).
        - html_content (str): The HTML content of the email message.
        - from_email (str): The email address of the sender. Defaults to `bot_email`.
        - subject (str): The subject of the email message. Defaults to "An email scheduled by LocalBot!".
        - time (int): The number of seconds to wait before sending the email message. Defaults to 126 seconds (i.e., 2 minutes and 6 seconds).

        ## Returns:
        - None: This function does not return a value.

        ## Raises:
        - Exception: If an error occurs while sending the email, this function raises an Exception with a descriptive error message.

        ## Example usage:
        >>> send_mail('user@example.com', '<p>Hello, world!</p>')
        """        
        message = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            html_content=html_content)
            
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            return f'Response: {response.status_code}'
        except Exception as e:
            print(e.to_dict)
        # except Exception as e:
        #     return e

bot = LocalBot()

date = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().strftime("%H:%M:%S")
def save_to_csv(client_name, client_email, client_category):
    """
    Saves the client information to a csv file.
    """
    try:
        with open('sentProposals.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([client_name, client_email, client_category, date, time])
    except Exception as e:
        print(e)




def load_emails_from_csv(file_name):
    """Load email addresses from a CSV file."""
    with open(file_name, 'r', newline='') as f:
        potential_clients = csv.DictReader(f)
        reader = []
        for row in potential_clients:
            row = dict(row)
            reader.append(row)
    potential_clients = reader

    return potential_clients


potential_clients = load_emails_from_csv('proposals.csv')
sent_emails = load_emails_from_csv('sentProposals.csv')


def load_emails_from_csv(file_name):
    """Load email addresses from a CSV file."""
    with open(file_name, 'r', newline='') as f:
        potential_clients = csv.DictReader(f)
        reader = []
        for row in potential_clients:
            row = dict(row)
            reader.append(row)
    potential_clients = reader

    return potential_clients



def find_duplicates(potential_clients):
    """Remove duplicate clients from the potential_clients list."""
    emails = {client["Email"] for client in sent_emails}
    duplicate_clients = [client for client in potential_clients if client["Email"] in emails]
    potential_clients[:] = [client for client in potential_clients if client not in duplicate_clients]

    if duplicate_clients:
        print(f'\nDUPLICATE - Removed from potential clients list:\n{[client["Email"] for client in duplicate_clients]}\n')

    return potential_clients

def send_proposals_to_clients(clients, messages, category):
    """Send proposals to clients based on the specified category."""
    if len(clients) > 0:
        print(f'\nSending proposals to {len(clients)} {category} clients...')
        for client in clients:
            message = messages[category].replace("<client_name>", client.get("company_name", client["Name"]))
            response = bot.send_mail(client["Email"], subject=subject, html_content=message)
            if str(response) != "HTTP Error 400: Bad Request":
                print(f'\nResponse {response}')
                print(f'\nResponse type {type(response)}')
                print(f'\nProposal sent to {client.get("company_name", client["Name"])}')
                save_to_csv(client.get("company_name", client["Name"]), client["Email"], client["Category"])
    else:
        print(f'\nNo {category} clients to send proposals to.')

# def send_proposals():
#     """Send proposals to potential clients."""
#     category_a = [client for client in potential_clients if client["Category"] == "Plumbing Services"]
#     category_b = [client for client in potential_clients if client["Category"] == "serviceProvider"]

#     find_duplicates(category_a)
#     find_duplicates(category_b)

#     send_proposals_to_clients(category_a, messages, "Plumbing Services")
#     send_proposals_to_clients(category_b, messages, "serviceProvider")

#     print("\nDone!")
def send_proposals():
    """Send proposals to potential clients."""
    unique_categories = set(client["Category"] for client in potential_clients)
    categorized_clients = {category: [] for category in unique_categories}

    for client in potential_clients:
        categorized_clients[client["Category"]].append(client)

    for category, clients in categorized_clients.items():
        find_duplicates(clients)
        send_proposals_to_clients(clients, messages, category)

    print("\nDone!")

if __name__ == "__main__":
    send_proposals()
