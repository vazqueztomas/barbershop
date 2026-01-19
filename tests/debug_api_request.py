"""
Test para simular exactamente la request HTTP del frontend
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from barbershop.main import app
import json


def test_create_haircut_api():
    """
    Simula exactamente la request que hace el frontend
    """
    client = TestClient(app)
    
    # Esto es lo que envía el frontend según el formulario
    frontend_data = {
        "clientName": "Juan Pérez",
        "serviceName": "Degradado",
        "price": 1500,
        "date": "2026-01-17"
    }
    
    print("=== REQUEST DEL FRONTEND ===")
    print(f"URL: POST http://localhost:8000/haircuts/create")
    print(f"Headers: Content-Type: application/json")
    print(f"Body: {json.dumps(frontend_data, indent=2)}")
    print()
    
    response = client.post("/haircuts/create", json=frontend_data)
    
    print("=== RESPONSE DEL BACKEND ===")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Body: {response.text}")
    print()
    
    if response.status_code != 200:
        print(f"ERROR: Status code {response.status_code}")
        try:
            error_detail = response.json()
            print(f"Error detail: {json.dumps(error_detail, indent=2)}")
        except:
            print(f"Response text: {response.text}")
    else:
        print("SUCCESS: Corte creado correctamente")
        print(f"Response: {response.json()}")
    
    return response


def test_create_haircut_with_all_fields():
    """
    Test con todos los campos incluyendo time
    """
    client = TestClient(app)
    
    data = {
        "clientName": "Juan Pérez",
        "serviceName": "Degradado",
        "price": 1500,
        "date": "2026-01-17",
        "time": "10:30"
    }
    
    print("\n=== TEST CON TIME ===")
    print(f"Body: {json.dumps(data, indent=2)}")
    print()
    
    response = client.post("/haircuts/create", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Body: {response.text}")
    
    return response


def test_create_haircut_with_empty_time():
    """
    Test con time vacío (como lo envía el formulario si no se completa)
    """
    client = TestClient(app)
    
    data = {
        "clientName": "Juan Pérez",
        "serviceName": "Degradado",
        "price": 1500,
        "date": "2026-01-17",
        "time": ""
    }
    
    print("\n=== TEST CON TIME VACÍO ===")
    print(f"Body: {json.dumps(data, indent=2)}")
    print()
    
    response = client.post("/haircuts/create", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Body: {response.text}")
    
    return response


def test_create_haircut_without_time():
    """
    Test sin el campo time (como lo envía el formulario modificado)
    """
    client = TestClient(app)
    
    data = {
        "clientName": "Juan Pérez",
        "serviceName": "Degradado",
        "price": 1500,
        "date": "2026-01-17"
    }
    
    print("\n=== TEST SIN CAMPO TIME ===")
    print(f"Body: {json.dumps(data, indent=2)}")
    print()
    
    response = client.post("/haircuts/create", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Body: {response.text}")
    
    return response


if __name__ == "__main__":
    print("=" * 70)
    print("TEST API: Crear corte con datos del frontend")
    print("=" * 70)
    test_create_haircut_api()
    
    print("\n" + "=" * 70)
    print("TEST API: Con campo time")
    print("=" * 70)
    test_create_haircut_with_all_fields()
    
    print("\n" + "=" * 70)
    print("TEST API: Con time vacío")
    print("=" * 70)
    test_create_haircut_with_empty_time()
    
    print("\n" + "=" * 70)
    print("TEST API: Sin campo time")
    print("=" * 70)
    test_create_haircut_without_time()
