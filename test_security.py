import requests
import io

BASE_URL = "http://localhost:5000/api/analyze"

def test_no_file():
    print("Test 1: No file provided")
    try:
        response = requests.post(BASE_URL)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 400
    except Exception as e:
        print(f"FAILED: {e}")

def test_invalid_extension():
    print("\nTest 2: Invalid extension (.txt)")
    files = {'image': ('test.txt', b'some content', 'text/plain')}
    try:
        response = requests.post(BASE_URL, files=files)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 400
    except Exception as e:
        print(f"FAILED: {e}")

def test_large_file():
    print("\nTest 3: Large file (>10MB)")
    # Create dummy large content (11MB)
    large_content = b'0' * (11 * 1024 * 1024)
    files = {'image': ('large.jpg', large_content, 'image/jpeg')}
    try:
        response = requests.post(BASE_URL, files=files)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 400
    except Exception as e:
        print(f"FAILED: {e}")

def test_corrupt_image():
    print("\nTest 4: Corrupt image file")
    files = {'image': ('corrupt.jpg', b'not an image', 'image/jpeg')}
    try:
        response = requests.post(BASE_URL, files=files)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 400
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_no_file()
    test_invalid_extension()
    test_large_file()
    test_corrupt_image()
