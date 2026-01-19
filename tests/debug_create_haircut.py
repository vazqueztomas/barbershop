"""
Test para debuggear la creación de un corte
Simula exactamente lo que el frontend envía
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from barbershop.models import HaircutCreate, Haircut
from barbershop.database import create_connection
from barbershop.repositories import HaircutRepository


def test_haircut_create_with_frontend_data():
    """
    Simula los datos que envía el frontend:
    {
        "clientName": "Juan Pérez",
        "serviceName": "Degradado",
        "price": 1500,
        "date": "2026-01-17"
    }
    """
    frontend_data = {
        "clientName": "Juan Pérez",
        "serviceName": "Degradado",
        "price": 1500,
        "date": "2026-01-17"
    }
    
    print("=== DATOS DEL FRONTEND ===")
    print(f"Tipo de clientName: {type(frontend_data['clientName'])}")
    print(f"Tipo de serviceName: {type(frontend_data['serviceName'])}")
    print(f"Tipo de price: {type(frontend_data['price'])}")
    print(f"Tipo de date: {type(frontend_data['date'])}")
    print(f"Contenido: {frontend_data}")
    print()
    
    # Intentar crear el objeto con el modelo del backend
    print("=== CREANDO HaircutCreate ===")
    try:
        haircut_create = HaircutCreate(**frontend_data)
        print(f"SUCCESS: HaircutCreate creado: {haircut_create}")
        print(f"  - clientName: {haircut_create.clientName}")
        print(f"  - serviceName: {haircut_create.serviceName}")
        print(f"  - price: {haircut_create.price}")
        print(f"  - date: {haircut_create.date} (tipo: {type(haircut_create.date)})")
        print(f"  - time: {haircut_create.time}")
    except Exception as e:
        print(f"ERROR al crear HaircutCreate: {e}")
        print(f"Tipo de excepción: {type(e)}")
        
        # Verificar cada campo individualmente
        print("\n=== VERIFICANDO CAMPOS INDIVIDUALMENTE ===")
        for key, value in frontend_data.items():
            print(f"  {key}: {value} (tipo: {type(value)})")
    
    print()
    
    # Test con base de datos real
    print("=== TEST CON BASE DE DATOS ===")
    conn = create_connection("testing.db")
    try:
        repo = HaircutRepository(conn)
        result = repo.create(haircut_create)
        print(f"SUCCESS: Corte creado con ID: {result.id}")
    except Exception as e:
        print(f"ERROR al guardar en base de datos: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pass  # No cerramos la conexión para poder verificar después


def test_all_possible_date_formats():
    """
    Testea diferentes formatos de fecha que podría enviar el frontend
    """
    test_cases = [
        ("YYYY-MM-DD string", "2026-01-17"),
        ("date object", date(2026, 1, 17)),
        ("ISO format string", "2026-01-17T00:00:00"),
    ]
    
    for name, date_value in test_cases:
        print(f"\n=== TEST: {name} ===")
        data = {
            "clientName": "Test Client",
            "serviceName": "Test Service",
            "price": 1000,
            "date": date_value
        }
        
        try:
            haircut = HaircutCreate(**data)
            print(f"SUCCESS: {haircut}")
        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("TEST 1: Datos del frontend")
    print("=" * 60)
    test_haircut_create_with_frontend_data()
    
    print("\n" + "=" * 60)
    print("TEST 2: Diferentes formatos de fecha")
    print("=" * 60)
    test_all_possible_date_formats()
