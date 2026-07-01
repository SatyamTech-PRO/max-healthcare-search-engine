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
        response = client.get("/api/search?q=CALSHINE")
        assert response.status_code == 200
        res = response.json()
        print(f"Results for CALSHINE: {res['total']}")
        assert res['total'] > 0

        print("Testing RapidFuzz (typo)...")
        # Intentional typo "CALSHIN"
        response = client.get("/api/search?q=CALSHIN")
        assert response.status_code == 200
        res = response.json()
        print(f"Results for CALSHIN: {res['total']}")
        
        # Check if the result contains the correct match
        names = [r["name"].lower() for r in res["results"]]
        found = any("calshine" in n for n in names)
        if found:
            print("RapidFuzz successfully found CALSHINE despite typo!")
        else:
            print("RapidFuzz failed to find CALSHINE for typo 'CALSHIN'. Names returned:", names)

        print("Testing /api/map-json endpoint...")
        payload = {
            "medication": [
                {"drugDesc": "CALSHIN"} # typo
            ],
            "investigationAdvised": [
                {"investigationAdvised": "CT Head Brain"} # generic match
            ],
            "procedureAdvised": [
                "ECG Review" # string item test
            ],
            "extraField": "should be ignored"
        }
        
        map_resp = client.post("/api/map-json", json=payload)
        assert map_resp.status_code == 200, f"Failed map-json: {map_resp.text}"
        map_data = map_resp.json()
        print(f"Mapping response: {map_data}")
        assert "medication" in map_data
        assert "investigationAdvised" in map_data
        assert "procedureAdvised" in map_data
        
        med_match = map_data["medication"][0]
        assert "calshine" in med_match["matched_name"].lower()
        assert med_match["match_type"] == "medicine"
        
        proc_match = map_data["procedureAdvised"][0]
        assert "ecg review" in proc_match["matched_name"].lower()
        assert proc_match["match_type"] == "procedure"

if __name__ == "__main__":
    run_tests()
    print("All backend tests passed!")
