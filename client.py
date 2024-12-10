import requests

SERVER_URL = 'http://192.168.1.1:8000/input'

def send_input(input_data):
    """
    Sends the input string to the FastAPI server.
    """
    try:
        payload = {"input": input_data}
        response = requests.post(SERVER_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print("Input sent successfully")
        else:
            print("Failed to send input")
            print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Failed to send input: {e}")

if __name__ == "__main__":
    print("Keyboard-over-Internet Client")
    print("Enter text to send (or 'exit' to quit):")

    while True:
        # Get user input
        user_input = input("Input: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        # Send the input to the server
        send_input(user_input)
