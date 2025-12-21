import requests
import unittest
import time

BASE_URL = 'http://127.0.0.1:5000'

class TestCoreFlow(unittest.TestCase):
    def setUp(self):
        # Create unique data to avoid conflicts
        self.timestamp = int(time.time())
        self.business_data = {
            "name": f"Test Business {self.timestamp}",
            "contact": "1234567890",
            "address": "123 Test St",
            "email": f"business{self.timestamp}@test.com",
            "password": "password123"
        }
        self.user_data = {
            "name": f"Test User {self.timestamp}",
            "email": f"user{self.timestamp}@test.com",
            "password": "password123",
            "phone": f"555{str(self.timestamp)[-7:]}",
            "dependents": 1
        }

    def test_full_flow(self):
        # 1. Create Business
        print("\n[1] Creating Business...")
        resp = requests.post(f"{BASE_URL}/api/businesses", json=self.business_data)
        self.assertEqual(resp.status_code, 201)
        business_id = resp.json()['id']
        print(f"    Business created with ID: {business_id}")

        # 2. Add Menu Item
        print("[2] Adding Menu Item...")
        menu_data = {
            "name": "Test Meal",
            "price": 10.0,
            "description": "Tasty test meal",
            "category": "Test",
            "available": True
        }
        resp = requests.post(f"{BASE_URL}/api/businesses/{business_id}/menu", json=menu_data)
        self.assertEqual(resp.status_code, 201)
        meal_id = resp.json()['meal']['id']
        print(f"    Menu Item added with ID: {meal_id}")

        # 3. Create User
        print("[3] Creating User...")
        resp = requests.post(f"{BASE_URL}/api/users", json=self.user_data)
        if resp.status_code != 201:
            print(f"FAILED to check user: {resp.text}")
        self.assertEqual(resp.status_code, 201)
        user_id = resp.json()['id']
        print(f"    User created with ID: {user_id}")

        # 4. Make Donation
        print("[4] Making Donation...")
        donation_data = {
            "donor_name": "Test Donor",
            "amount": 50.0,
            "business_id": business_id
        }
        resp = requests.post(f"{BASE_URL}/api/donations", json=donation_data)
        self.assertEqual(resp.status_code, 201)
        new_balance = resp.json()['new_balance']
        self.assertEqual(float(new_balance), 50.0)
        print(f"    Donation successful. New Business Balance: {new_balance}")

        # 5. Claim Meal
        print("[5] Claiming Meal...")
        claim_data = {"menu_id": meal_id}
        resp = requests.post(f"{BASE_URL}/api/users/{user_id}/claim_meal", json=claim_data)
        self.assertEqual(resp.status_code, 201)
        final_balance = resp.json()['new_balance']
        self.assertEqual(float(final_balance), 40.0) # 50 - 10
        print(f"    Meal claimed successfully. Final Business Balance: {final_balance}")

        # 6. Verify Limit (Try to claim more than limit)
        # User has 2 + 2*1 = 4 meals limit. 
        # Claim 3 more times should be OK, 4th fail?
        # Current logic: claimed_today >= meal_cap
        # Currently claimed: 1. Limit: 4.
        
        print("[6] Checking limits...")
        for i in range(3):
            requests.post(f"{BASE_URL}/api/users/{user_id}/claim_meal", json=claim_data)
        
        # 5th attempt (1 initial + 3 loop = 4 claimed so far. 5th should fail?)
        # Wait, limit is 4. If claimed_today (4) >= meal_cap (4), then 5th request should fail.
        resp = requests.post(f"{BASE_URL}/api/users/{user_id}/claim_meal", json=claim_data)
        print(f"    Over-limit claim status: {resp.status_code}")
        self.assertEqual(resp.status_code, 403)

if __name__ == '__main__':
    unittest.main()
