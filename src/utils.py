import random
import string

# Function to generate a random order ID
def generate_order_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Function to sanitize inputs
def sanitize_input(input_value):
    # Sanitize input_value here (e.g., remove special characters, escape characters)
    return input_value