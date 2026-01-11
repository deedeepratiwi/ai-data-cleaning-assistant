import os
import time
import requests

def test_end_to_end():
    # 1. Prepare test CSV
    test_csv = "tests/test_dirty.csv"
    with open(test_csv, "w") as f:
        f.write("name,age\nAlice,\nBob,30\nAlice,\n")

    # 2. Upload file
    with open(test_csv, "rb") as f:
        resp = requests.post("http://localhost:8000/jobs/upload", files={"file": f})
    assert resp.status_code == 200
    job_id = resp.json()["job_id"]

    # 3. Start profiling (triggers pipeline)
    resp = requests.post(f"http://localhost:8000/jobs/{job_id}/profile")
    assert resp.status_code == 202

    # 4. Poll for job completion
    status = "profiling"
    for _ in range(30):
        time.sleep(1)
        resp = requests.get(f"http://localhost:8000/jobs/{job_id}")
        assert resp.status_code == 200
        status = resp.json()["status"]
        if status == "done":
            break
    assert status == "done"

    # 5. Download cleaned CSV
    resp = requests.get(f"http://localhost:8000/jobs/{job_id}/download")
    assert resp.status_code == 200
    cleaned_csv = resp.content.decode()
    assert "Alice" in cleaned_csv and "Bob" in cleaned_csv

    # 6. Download report
    resp = requests.get(f"http://localhost:8000/jobs/{job_id}/report")
    assert resp.status_code == 200
    report = resp.content.decode()
    assert "Cleaning Report" in report

    print("End-to-end test passed.")
