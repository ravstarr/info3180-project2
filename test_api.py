import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_backend():
    session = requests.Session()
    
    # 1. Register User 1
    print("Registering User 1...")
    resp = session.post(f"{BASE_URL}/register", json={"email": "user1@example.com", "password": "password123"})
    print(resp.status_code, resp.json())
    
    # 2. Register User 2
    print("\nRegistering User 2...")
    resp = session.post(f"{BASE_URL}/register", json={"email": "user2@example.com", "password": "password123"})
    print(resp.status_code, resp.json())

    # 3. Login User 1
    print("\nLogging in User 1...")
    resp = session.post(f"{BASE_URL}/login", json={"email": "user1@example.com", "password": "password123"})
    print(resp.status_code, resp.json())
    
    # 4. Create Profile User 1
    print("\nCreating Profile for User 1...")
    profile_data = {
        "name": "Alice",
        "age": 25,
        "bio": "I love hiking and coding.",
        "location": "Kingston",
        "interests": ["hiking", "coding", "music"],
        "looking_for": "friendship"
    }
    resp = session.put(f"{BASE_URL}/profile", json=profile_data)
    print(resp.status_code, resp.json())

    # 5. Get Me
    print("\nGetting current user (Me)...")
    resp = session.get(f"{BASE_URL}/me")
    print(resp.status_code, resp.json())
    
    # 6. Login User 2
    session2 = requests.Session()
    print("\nLogging in User 2...")
    resp = session2.post(f"{BASE_URL}/login", json={"email": "user2@example.com", "password": "password123"})
    print(resp.status_code, resp.json())
    user2_id = resp.json()['user_id']
    
    # 7. Create Profile User 2
    print("\nCreating Profile for User 2...")
    profile_data2 = {
        "name": "Bob",
        "age": 27,
        "bio": "Adventurer and coffee lover.",
        "location": "Kingston",
        "interests": ["hiking", "coffee", "travel"],
        "looking_for": "friendship"
    }
    resp = session2.put(f"{BASE_URL}/profile", json=profile_data2)
    print(resp.status_code, resp.json())

    # 8. Potential Matches for User 1
    print("\nPotential Matches for User 1...")
    resp = session.get(f"{BASE_URL}/potential-matches")
    print(resp.status_code, resp.json())
    
    # 9. User 1 likes User 2
    print("\nUser 1 likes User 2...")
    resp = session.post(f"{BASE_URL}/like/{user2_id}")
    print(resp.status_code, resp.json())
    
    # 10. User 2 likes User 1
    print("\nUser 2 likes User 1...")
    user1_id = session.get(f"{BASE_URL}/me").json()['id']
    resp = session2.post(f"{BASE_URL}/like/{user1_id}")
    print(resp.status_code, resp.json())
    
    # 11. Check Matches for User 1
    print("\nChecking Matches for User 1...")
    resp = session.get(f"{BASE_URL}/matches")
    print(resp.status_code, resp.json())
    match_id = resp.json()[0]['match_id']
    
    # 12. Send Message User 1 to User 2
    print("\nUser 1 sends message to User 2...")
    resp = session.post(f"{BASE_URL}/messages/{match_id}", json={"content": "Hi Bob! Ready for a hike?"})
    print(resp.status_code, resp.json())
    
    # 13. Get Messages for User 2
    print("\nUser 2 gets messages...")
    resp = session2.get(f"{BASE_URL}/messages/{match_id}")
    print(resp.status_code, resp.json())

if __name__ == "__main__":
    test_backend()
