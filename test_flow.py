import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_flow():
    print("Testing Organization Flow...")
    
    # 1. Register Business
    business_data = {
        "name": "Test Org " + str(requests.get(BASE_URL).status_code), # uniqueish
        "contact": "1234567890",
        "email": "testorg@example.com",
        "password": "password123",
        "type": "ngo",
        "address": "123 Test St",
        "people_count": 50,
        "needs": "Food"
    }
    
    # Use a unique email
    import time
    business_data['email'] = f"testorg{int(time.time())}@example.com"
    business_data['name'] = f"Test Org {int(time.time())}"

    print(f"Registering {business_data['email']}...")
    res = requests.post(f"{BASE_URL}/businesses/register", json=business_data)
    if res.status_code != 201:
        print("Registration Failed:", res.text)
        return
    
    org_id = res.json()['id']
    print(f"Registered Org ID: {org_id}")

    # 2. Login
    print("Testing Login...")
    login_data = {
        "email": business_data['email'],
        "password": "password123",
        "type": "business"
    }
    res = requests.post(f"{BASE_URL}/api/login", json=login_data)
    if res.status_code == 200:
        print("Login Successful:", res.json())
    else:
        print("Login Failed:", res.text)
        return

    # 3. Update Profile
    print("Testing Profile Update...")
    update_data = {
        "needs": "Updated Needs Description"
    }
    res = requests.put(f"{BASE_URL}/api/businesses/{org_id}", json=update_data)
    if res.status_code == 200:
        print("Update Successful:", res.json()['needs'])
        if res.json()['needs'] == "Updated Needs Description":
             print("Verification: Needs matched!")
    else:
        print("Update Failed:", res.text)

    # 4. Get Dashboard Data (Donations)
    print("Testing Get Donations...")
    res = requests.get(f"{BASE_URL}/api/donations/business/{org_id}")
    if res.status_code == 200:
        print("Fetch Donations Successful:", res.json())
    else:
        print("Fetch Donations Failed:", res.text)

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print("Error connecting to server. Is it running? ", e)
