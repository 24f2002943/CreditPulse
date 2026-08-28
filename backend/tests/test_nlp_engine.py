import pytest
from backend.app.ml.nlp_engine import nlp_engine

def test_nlp_negotiation_analysis():
    # Constructive cooperative transcript
    good_text = "Supplier and buyer mutually agreed to extend contract terms for 2 years with 2% discount."
    good_res = nlp_engine.analyze_transcript(good_text, "negotiation")
    assert good_res["sentiment_score"] > 0.0
    assert good_res["risk_flag_score"] < 0.3

    # Hostile dispute transcript
    bad_text = "Client issued formal breach notice and refused payment due to severe delivery default."
    bad_res = nlp_engine.analyze_transcript(bad_text, "service_failure")
    assert bad_res["sentiment_score"] < 0.0
    assert bad_res["risk_flag_score"] > 0.5

def test_relationship_history_scoring():
    history = [
        {"transcript_text": "Minor delay on shipment.", "interaction_type": "service_failure"},
        {"transcript_text": "Supplier provided immediate replacement tooling and client confirmed full satisfaction.", "interaction_type": "service_recovery"},
        {"transcript_text": "Annual supply framework contract renewed with mutual agreement.", "interaction_type": "negotiation"}
    ]
    rel = nlp_engine.compute_relationship_score(history)
    assert rel["relationship_score"] > 65.0
    assert rel["failure_resolution_rate"] == 1.0
    assert rel["relationship_band"] in ["strong_partner", "stable"]
