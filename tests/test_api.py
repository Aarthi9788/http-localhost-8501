from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "LegalEase"


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_document_types():

    response = client.get(
        "/document-types"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        len(data["document_types"])
        >= 5
    )


def test_generate_demo():

    response = client.post(
        "/generate",

        json={
            "document_type":
                "Non-Disclosure Agreement",

            "parties":
                "Company A and Company B",

            "terms":
                "Confidential information; "
                "No disclosure; "
                "Agreement lasts for two years",

            "effective_date":
                "2026-09-24",

            "jurisdiction":
                "Tamil Nadu, India",

            "additional_instructions":
                "Use numbered clauses"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "document" in data

    assert (
        data["document_type"]
        == "Non-Disclosure Agreement"
    )