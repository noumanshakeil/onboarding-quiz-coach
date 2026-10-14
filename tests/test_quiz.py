import pytest
@pytest.mark.asyncio
async def test_quiz(client):
    q = await client.post("/api/questions", json={"prompt": "VPN required?", "answer": "yes", "topic": "security"})
    qid = q.json()["id"]
    bad = await client.post(f"/api/questions/{qid}/attempt", json={"response": "no"})
    assert bad.json()["correct"] is False
    good = await client.post(f"/api/questions/{qid}/attempt", json={"response": "yes"})
    assert good.json()["correct"] is True
