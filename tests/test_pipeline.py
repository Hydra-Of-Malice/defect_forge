"""Pipeline tests on a fake Meta transport: inspector sanitizer, a full forge run, export, and the demo-mode API."""
import io
import json
import time
import zipfile

import cv2
import numpy as np
from PIL import Image

import app.forge.locate as locate
import app.inspect.inspector as inspector
import app.runs as runs
from app.export.coco import export_run
from app.forge.spec import DEFAULT_SPEC

TAX = {"part_name": "hazelnut", "part_width_mm": 20, "defects": [
    {"defect_type": "hole", "clause": "4.1", "description": "a small dark hole", "severity_note": "any"},
    {"defect_type": "print", "clause": "4.4", "description": "a small ink stamp", "severity_note": "any"}]}


def fake_sam(img, *, text=None, boxes=None, points=None, run_id=None, op="segment"):
    w, h = img.size
    m = np.zeros((h, w), bool)
    if boxes:
        x0, y0, x1, y1 = boxes[0]
        m[y0:y1, x0:x1] = True
    else:
        m = locate.otsu_mask(img)
    return {"objects": [{"object_id": "1", "box": None, "mask": m, "confidence": 0.9}], "ms": 1, "cost_usd": 0.0}


def fake_edit(png, prompt, **kw):
    a = np.array(Image.open(io.BytesIO(png)).convert("RGB"))
    h, w = a.shape[:2]
    cv2.circle(a, (w // 2, h // 2), 12, (15, 10, 8), -1)
    a = cv2.resize(a, (int(w * 1.5), int(h * 1.5)))
    buf = io.BytesIO()
    Image.fromarray(a).save(buf, "PNG")
    return {"images": [buf.getvalue()], "ms": 1, "cost_usd": 0.0}


def fake_critic(*a, **k):
    return {"realism": 5, "matches_type": True, "artifacts": "", "verdict": "accept", "revised_prompt": "", "cost_usd": 0.0, "ms": 1}


def fake_spark(messages, schema, name, **kw):
    return {"data": {"defect": True, "type": "hole", "has_box": True, "x0": 400, "y0": 400, "x1": 600, "y1": 600,
                     "confidence": 0.9, "rationale": "dark hole"}, "ms": 1, "cost_usd": 0.0, "usage": {}}


def test_inspector_box_scaling_and_sanitizer(monkeypatch):
    monkeypatch.setattr(inspector, "spark_json", fake_spark)
    img = Image.new("RGB", (1000, 500), (120, 60, 30))
    monkeypatch.setattr(inspector, "sam_segment", lambda *a, **k: {"objects": [{"mask": np.zeros((500, 1000), bool)}], "cost_usd": 0.0})
    r = inspector.inspect(img, DEFAULT_SPEC, ["hole"])
    assert r["box_px"] == [400, 200, 600, 300]
    assert r["verdict"] == "uncertain"          # claimed defect, but SAM found nothing in the box
    m = np.zeros((500, 1000), bool)
    m[220:280, 450:550] = True
    monkeypatch.setattr(inspector, "sam_segment", lambda *a, **k: {"objects": [{"mask": m}], "cost_usd": 0.0})
    assert inspector.inspect(img, DEFAULT_SPEC, ["hole"])["verdict"] == "defect"


def test_full_forge_run_on_fake_transport(monkeypatch):
    monkeypatch.setattr(runs, "image_edit", fake_edit)
    monkeypatch.setattr(runs, "sam_segment", fake_sam)
    monkeypatch.setattr(runs, "critic", fake_critic)
    monkeypatch.setattr(locate, "sam_segment", fake_sam)
    monkeypatch.setattr(inspector, "spark_json", fake_spark)
    monkeypatch.setattr(runs, "DEMO_MODE", False)
    pid = "sample-hazelnut_gen_01"
    rid = runs.manager.create(DEFAULT_SPEC, TAX, [pid], per_type=1, stress=True)
    run = runs.manager.get(rid)
    for _ in range(300):
        if run.data["status"] != "running":
            break
        time.sleep(0.1)
    assert run.data["status"] == "completed", run.events[-3:]
    acc = [s for s in run.data["samples"] if s["status"] == "accepted"]
    assert len(acc) == 2
    s = acc[0]
    assert all(v["passed"] for v in s["validators"] if v["hard"])
    assert s["size_mm"] and s["sam_iou"] is not None
    assert len(run.data["severity"]) == 2 * 7 and run.data["curves"]
    names = {e["event"] for e in run.events}
    assert {"run_started", "sample", "stage", "severity", "curves", "stress_completed", "run_completed"} <= names
    z = zipfile.ZipFile(io.BytesIO(export_run(run.dir, run.data)))
    coco = json.loads(z.read("annotations.json"))
    assert len(coco["images"]) == 2 and len(coco["annotations"]) == 2
    assert "evaluation" in coco["info"]["intended_use"]


def test_demo_mode_api_routes():
    from fastapi.testclient import TestClient
    from app.main import app
    c = TestClient(app)
    h = c.get("/api/health").json()
    assert h["demo_mode"] is True and "sam-3.1" in h["models"]
    assert "HAZELNUT" in c.get("/api/default-spec").json()["spec_text"]
    parts = c.get("/api/parts").json()["parts"]
    assert any(p["id"].startswith("sample-hazelnut_gen") for p in parts)
    assert c.get("/api/runs/does-not-exist").status_code == 404
    ev = c.get("/api/eval").json()
    assert "curves" in ev
