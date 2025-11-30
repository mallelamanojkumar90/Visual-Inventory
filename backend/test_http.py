import requests
import os

PROJECT_REF = "qbxuqzrayegzixuxleoa"
URL = f"https://{PROJECT_REF}.supabase.co/rest/v1/"

try:
    response = requests.get(URL, timeout=5)
    print(f"HTTPS Connection Status: {response.status_code}")
    print("HTTPS is reachable!")
except Exception as e:
    print(f"HTTPS Connection Failed: {e}")
