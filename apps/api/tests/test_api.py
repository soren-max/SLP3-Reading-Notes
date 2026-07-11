import importlib


def test_seeded_api_contract(tmp_path, monkeypatch):
    db_path = tmp_path / "test_slp3_notes.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    database = importlib.import_module("app.database")
    seed_module = importlib.import_module("app.seed")
    main_module = importlib.import_module("app.main")

    seed_module.seed()

    from fastapi.testclient import TestClient

    client = TestClient(main_module.app)

    sources = client.get("/api/sources")
    assert sources.status_code == 200
    source_data = sources.json()
    assert source_data[0]["title"] == "Speech and Language Processing, Third Edition draft"
    assert source_data[0]["type"] == "book"

    chapters = client.get("/api/chapters")
    assert chapters.status_code == 200
    chapter_data = chapters.json()
    assert len(chapter_data) == len(seed_module.CHAPTERS)

    high_priority_titles = {chapter["title"] for chapter in chapter_data if chapter["priority"] == "高"}
    expected_high_priority = {
        "Embeddings",
        "Large Language Models",
        "Transformers",
        "Post-training",
        "Retrieval-based Models",
        "Sequence Labeling for POS and Named Entities",
        "Information Extraction",
        "Semantic Role Labeling",
        "Coreference Resolution and Entity Linking",
    }
    assert expected_high_priority.issubset(high_priority_titles)

    notes = client.get("/api/notes")
    assert notes.status_code == 200
    assert len(notes.json()) == len(seed_module.CHAPTERS)
    chapter_9 = next(chapter for chapter in chapter_data if chapter["number"] == 9)
    chapter_9_note = next(note for note in notes.json() if note["chapter_id"] == chapter_9["id"])
    assert "Masked Language Modeling" in chapter_9_note["content"]
    assert "KG-RAG" in chapter_9_note["content"]
    chapter_10 = next(chapter for chapter in chapter_data if chapter["number"] == 10)
    chapter_10_note = next(note for note in notes.json() if note["chapter_id"] == chapter_10["id"])
    assert "Direct Preference Optimization" in chapter_10_note["content"]
    assert "Test-Time Compute" in chapter_10_note["content"]
    chapter_11 = next(chapter for chapter in chapter_data if chapter["number"] == 11)
    chapter_11_note = next(note for note in notes.json() if note["chapter_id"] == chapter_11["id"])
    assert "Dense Retrieval" in chapter_11_note["content"]
    assert "KG-RAG" in chapter_11_note["content"]
    chapter_17 = next(chapter for chapter in chapter_data if chapter["number"] == 17)
    chapter_17_note = next(note for note in notes.json() if note["chapter_id"] == chapter_17["id"])
    assert "Conditional Random Field" in chapter_17_note["content"]
    assert "entity linking" in chapter_17_note["content"]
    chapter_20 = next(chapter for chapter in chapter_data if chapter["number"] == 20)
    chapter_20_note = next(note for note in notes.json() if note["chapter_id"] == chapter_20["id"])
    assert "Event Extraction" in chapter_20_note["content"]
    assert "Temporal Analysis" in chapter_20_note["content"]
    chapter_21 = next(chapter for chapter in chapter_data if chapter["number"] == 21)
    chapter_21_note = next(note for note in notes.json() if note["chapter_id"] == chapter_21["id"])
    assert "Semantic Role Labeling" in chapter_21_note["content"]
    assert "PropBank" in chapter_21_note["content"]

    roadmap = client.get("/api/roadmap").json()
    roadmap_steps = " ".join(step for phase in roadmap["slp3"] for step in phase["steps"])
    custom_routes = " ".join(route["name"] for route in roadmap["custom"])
    assert "KG-RAG" in roadmap_steps
    assert "GraphRAG" in roadmap_steps
    assert "Entity Linking" in roadmap_steps
    assert "GraphRAG 论文路线" in custom_routes

    report = client.get("/api/report?source_id=1").json()
    assert report["progress_percent"] > 0
    assert "老师您好" in report["wechat_text"]

    progress = client.patch("/api/chapters/1/progress", json={"status": "阅读中"})
    assert progress.status_code == 200
    assert progress.json()["status"] == "阅读中"

    created = client.post(
        "/api/notes",
        json={"source_id": 1, "chapter_id": 1, "title": "API test note", "content": "# API test", "tags": "test,KG"},
    )
    assert created.status_code == 201
    note_id = created.json()["id"]

    updated = client.patch(f"/api/notes/{note_id}", json={"title": "API test note updated"})
    assert updated.status_code == 200
    assert updated.json()["title"] == "API test note updated"

    deleted = client.delete(f"/api/notes/{note_id}")
    assert deleted.status_code == 204

    database.Base.metadata.drop_all(bind=database.engine)
