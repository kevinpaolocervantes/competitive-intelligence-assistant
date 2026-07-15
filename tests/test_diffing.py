from src.diffing import compare_runs


def test_detects_changed_page():
    previous = {"pages": [{"url": "https://example.com", "text": "Old message", "content_hash": "a"}]}
    current = {"pages": [{"url": "https://example.com", "text": "New message", "content_hash": "b"}]}
    changes = compare_runs(previous, current)
    assert len(changes) == 1
    assert changes[0]["status"] == "changed"
    assert "New message" in changes[0]["diff"]


def test_baseline_run():
    current = {"pages": [{"url": "https://example.com", "text": "Hello", "content_hash": "x"}]}
    changes = compare_runs(None, current)
    assert changes[0]["status"] == "baseline"
