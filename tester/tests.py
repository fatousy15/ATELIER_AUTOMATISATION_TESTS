from tester.client import get

def test_status_200():
    response, latency = get("/", params={"name": "michael"})
    assert response.status_code == 200, "Status code should be 200"
    return {"name": "test_status_200", "status": "PASS", "latency_ms": latency}

def test_content_type_json():
    response, latency = get("/", params={"name": "michael"})
    assert "application/json" in response.headers.get("Content-Type", "")
    return {"name": "test_content_type_json", "status": "PASS", "latency_ms": latency}

def test_field_name_present():
    response, latency = get("/", params={"name": "michael"})
    data = response.json()
    assert "name" in data, "Field 'name' missing"
    return {"name": "test_field_name_present", "status": "PASS", "latency_ms": latency}

def test_field_age_present():
    response, latency = get("/", params={"name": "michael"})
    data = response.json()
    assert "age" in data, "Field 'age' missing"
    return {"name": "test_field_age_present", "status": "PASS", "latency_ms": latency}

def test_field_count_is_int():
    response, latency = get("/", params={"name": "michael"})
    data = response.json()
    assert isinstance(data["count"], int), "Field 'count' should be int"
    return {"name": "test_field_count_is_int", "status": "PASS", "latency_ms": latency}

def test_field_name_is_string():
    response, latency = get("/", params={"name": "michael"})
    data = response.json()
    assert isinstance(data["name"], str), "Field 'name' should be string"
    return {"name": "test_field_name_is_string", "status": "PASS", "latency_ms": latency}

def test_with_country():
    response, latency = get("/", params={"name": "anna", "country_id": "FR"})
    assert response.status_code == 200
    return {"name": "test_with_country", "status": "PASS", "latency_ms": latency}

def test_empty_name():
    response, latency = get("/", params={"name": ""})
    assert response.status_code in [200, 422, 400]
    return {"name": "test_empty_name", "status": "PASS", "latency_ms": latency}

def run_all():
    tests = [
        test_status_200,
        test_content_type_json,
        test_field_name_present,
        test_field_age_present,
        test_field_count_is_int,
        test_field_name_is_string,
        test_with_country,
        test_empty_name,
    ]
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            results.append({
                "name": test.__name__,
                "status": "FAIL",
                "latency_ms": 0,
                "details": str(e)
            })
    return results
