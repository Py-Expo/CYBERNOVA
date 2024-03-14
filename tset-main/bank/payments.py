import stripe
import os

# Set your Stripe secret key from environment variable
os.environ['STRIPE_SECRET_KEY'] = 'sk_test_51Os3JJSBcgtj4kLbcLYbyclhFjBhDKHAhFqXFgW33jlKIAwFNpKD8Mduc5VxxZgdvbyyT43YU2JxTxjknDERPOD4007oQrpYgg'
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Function to create a bank account token for a given bank account details
def create_bank_account_token(account_number, ifsc_code):
    try:
        # Create a token using bank account details
        token = stripe.Token.create(
            bank_account={
                'country': 'IN',
                'currency': 'inr',
                'account_number': account_number,
                'routing_number': ifsc_code,
            }
        )
        return token
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        print("Stripe error:", e)
        return None

# Function to initiate a transfer between bank accounts
def initiate_transfer(amount,sender_account_number, sender_ifsc_code,recipient_account_number, recipient_ifsc_code):
    try:
        # Create a transfer from sender's bank account to recipient's bank account
        transfer = stripe.Transfer.create(
            amount=amount * 100,  # Amount in cents
            currency='inr',       # Currency code
            source_transaction=create_bank_account_token(sender_account_number, sender_ifsc_code).id,  # Source of funds (sender's bank account)
            destination=create_bank_account_token(recipient_account_number, recipient_ifsc_code).id,      # Destination of funds (recipient's bank account)
            description='Transfer between bank accounts'
        )
        print("Transfer initiated successfully:", transfer.id)
        return transfer
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        print("stripe error:",e)
        return None

# Example usage:
def main():
    # Replace with actual bank account details
    sender_account_number = '000123456789'
    sender_ifsc_code = 'HDFC0000261'
    recipient_account_number = '000123456789'
    recipient_ifsc_code = 'HDFC0000261'
    amount = 10  # Amount in INR
    initiate_transfer(amount,sender_account_number,sender_ifsc_code,recipient_account_number,recipient_ifsc_code)

if __name__ == "_main_":
    main()