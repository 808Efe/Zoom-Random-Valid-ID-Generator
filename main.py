import random
import requests
import threading
import hashlib
import time

# Replace YOUR_API_KEY and YOUR_API_SECRET with your actual API key and secret
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

# Set the base URL for the Zoom API
base_url = "https://api.zoom.us/v2"

# Set the headers for the request
headers = {
  "Authorization": f"Basic {api_key}:{api_secret}"
}

def get_room_name(room_id):
  # Send a GET request to the /meetings/{meetingId} endpoint
  response = requests.get(f"{base_url}/meetings/{room_id}", headers=headers)
  
  # If the response status code is 200, return the name of the room
  if response.status_code == 200:
    return response.json()["topic"]
  else:
    return "Invalid room ID"

def generate_zoom_room_id(invalid_count):
  while True:
    # Get the current date and time
    message = str(time.time())
    
    # Generate the hash of the message
    hash = hashlib.sha1(message.encode()).hexdigest()
    
    # Take the first 9 digits of the hash as the room ID
    room_id = hash[:9]
    
    # Add a hyphen after the third and sixth digits
    room_id = room_id[:3] + '-' + room_id[3:6] + '-' + room_id[6:]
    
    # Get the name of the room
    room_name = get_room_name(room_id)
    
    # If the room ID is valid, print it and its name
    if room_name != "Invalid room ID":
      print(f"{room_id}: {room_name}")
      break
    else:
      # If the room ID is invalid, print the number of invalid IDs that have been generated
      invalid_count += 1
      print(f"{invalid_count} invalid room IDs generated")

# Test the function with multiple threads
invalid_count = 0
threads = []
for i in range(10):
  t = threading.Thread(target=generate_zoom_room_id, args=(invalid_count,))
  threads.append(t)
  t.start()
