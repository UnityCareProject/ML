import requests

# Define the API endpoint URL
api_url = f'http://localhost:5000/question'
# Ask the user for input
question = input('Enter your question: ')

    # Create the request payload
payload = {
    'question': question
}

# Make a POST request to the API endpoint
response = requests.post(api_url, json=payload)
# Check the response status code
if response.status_code == 200:
# Extract the content from the response
    result = response.json()
    content = result['content']
        
        # Use the content in your application
    print(content)
else:
    print('Error occurred while calling the API.')