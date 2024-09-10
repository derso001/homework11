import requests

url = "http://127.0.0.1:8000/contacts"

# Дані для створення нового контакту
contact_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone_number": "123-456-7890",
    "birthday": "1990-01-01",
    "additional_info": "Friend from college"
}

# Відправка POST-запиту
response = requests.post(url, json=contact_data)

# Перевірка статусу відповіді
if response.status_code == 201:
    print("Contact created successfully!")
    print("Response data:", response.json())
else:
    print(f"Failed to create contact. Status code: {response.status_code}")
    print("Response content:", response.content)