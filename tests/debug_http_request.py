"""
Test para debuggear la request HTTP real al backend
"""
import requests
import json


def test_real_api():
    """
    Hace una request real al backend
    """
    # Primero iniciar el backend: uvicorn barbershop.main:app --reload
    
    base_url = "http://127.0.0.1:8000"
    
    # Datos que envía el frontend
    frontend_data = {
        "clientName": "Juan Pérez",
        "serviceName": "Degradado",
        "price": 1500,
        "date": "2026-01-17"
    }
    
    print("=" * 70)
    print("REQUEST HTTP REAL AL BACKEND")
    print("=" * 70)
    print(f"URL: {base_url}/haircuts/create")
    print(f"Method: POST")
    print(f"Headers: Content-Type: application/json")
    print(f"Body: {json.dumps(frontend_data, indent=2)}")
    print()
    
    try:
        response = requests.post(
            f"{base_url}/haircuts/create",
            json=frontend_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print("=" * 70)
        print("RESPONSE")
        print("=" * 70)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Body: {response.text}")
        
        if response.status_code == 200:
            print("\nSUCCESS!")
            print(f"Response: {response.json()}")
        else:
            print(f"\nERROR: Status {response.status_code}")
            try:
                error = response.json()
                print(f"Error detail: {json.dumps(error, indent=2)}")
            except:
                print(f"Raw response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("ERROR: No se pudo conectar al backend")
        print("Asegurate de que el backend esté corriendo: uvicorn barbershop.main:app --reload")
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    test_real_api()
