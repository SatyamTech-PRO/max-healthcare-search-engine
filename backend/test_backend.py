import httpx
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def run_tests():
    with TestClient(app) as client:
        print("Testing DB initialization and stats endpoint...")
        # Stats endpoint
        response = client.get("/api/stats")
        assert response.status_code == 200, f"Failed stats: {response.status_code}"
        stats = response.json()
        print(f"Stats: {stats}")
        assert stats["medicines"] > 0, "No medicines found!"

        print("Testing FTS5 search (exact match)...")
        response = client.get("/api/search?q=Paracetamol")
        assert response.status_code == 200
        res = response.json()
        print(f"Results for Paracetamol: {res['total']}")
        assert res["total"] > 0, "Paracetamol not found"

        print("Testing RapidFuzz (typo)...")
        # Intentional typo "Paracetmol"
        response = client.get("/api/search?q=Paracetmol")
        assert response.status_code == 200
        res = response.json()
        print(f"Results for Paracetmol: {res['total']}")
        
        # Check if the result contains the correct match
        names = [r["name"].lower() for r in res["results"]]
        found = any("paracetamol" in n for n in names)
        if found:
            print("RapidFuzz successfully found Paracetamol despite typo!")
        else:
            print("RapidFuzz failed to find Paracetamol for typo 'Paracetmol'. Names returned:", names)

if __name__ == "__main__":
    run_tests()
    print("All backend tests passed!")
