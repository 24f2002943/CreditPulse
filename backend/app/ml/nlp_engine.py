import re
from typing import Dict, Any, List, Optional
from datetime import datetime

# Domain-specific financial/B2B behavioral lexicons
DISPUTE_KEYWORDS = [
    "breach", "penalty", "liquidated damages", "lawyer", "legal notice",
    "withhold payment", "withheld", "default", "overdue", "refused payment",
    "litigation", "arbitration", "demand letter", "cancel contract", "terminate agreement"
]

FRICTION_KEYWORDS = [
    "extension", "delay", "postpone", "cash crunch", "liquidity constraint",
    "shortage", "discount requested", "defect", "rejection", "unacceptable",
    "failure", "escalation", "surcharge dispute", "re-tender", "stalled"
]

COOPERATIVE_KEYWORDS = [
    "renewed", "extended", "satisfaction", "resolved", "compromise",
    "partnership", "early payment", "discount agreed", "verified quality",
    "recovered", "long-term", "mutually agreed", "on-time", "repaired"
]

class NLPRelationshipEngine:
    """
    NLP Engine for B2B relationship health, negotiation friction, and service recovery scoring.
    Transforms unstructured interaction logs into quantifiable credit risk signals.
    """

    def analyze_transcript(self, text: str, interaction_type: str = "negotiation") -> Dict[str, Any]:
        """
        Analyzes an interaction transcript for sentiment, dispute risk, and behavioral signals.
        """
        lower_text = text.lower()

        # Keyword intensity counting
        dispute_hits = sum(1 for kw in DISPUTE_KEYWORDS if kw in lower_text)
        friction_hits = sum(1 for kw in FRICTION_KEYWORDS if kw in lower_text)
        coop_hits = sum(1 for kw in COOPERATIVE_KEYWORDS if kw in lower_text)

        # Baseline Sentiment Calculation (-1.0 to +1.0)
        net_tone = (coop_hits * 1.5) - (dispute_hits * 2.5) - (friction_hits * 1.2)
        total_signals = coop_hits + dispute_hits + friction_hits
        
        if total_signals == 0:
            sentiment_score = 0.1  # Slight neutral positive
            risk_flag_score = 0.15
        else:
            sentiment_score = max(-1.0, min(1.0, net_tone / max(total_signals * 1.5, 1.0)))
            # Risk flag is higher when dispute and friction are high
            raw_risk = (dispute_hits * 0.40) + (friction_hits * 0.20) - (coop_hits * 0.15)
            risk_flag_score = max(0.02, min(0.98, raw_risk + 0.15))

        # Interaction Type Contextual Modifiers
        if interaction_type == "service_failure":
            risk_flag_score = min(0.98, risk_flag_score + 0.25)
            sentiment_score = min(sentiment_score, -0.30)
        elif interaction_type == "service_recovery":
            # If recovery contains cooperative resolution, reward the score
            if coop_hits > 0 or sentiment_score > -0.2:
                risk_flag_score = max(0.05, risk_flag_score * 0.45)
                sentiment_score = max(0.20, sentiment_score + 0.40)

        # Highlight key detected risk phrases
        detected_flags = [kw for kw in DISPUTE_KEYWORDS + FRICTION_KEYWORDS if kw in lower_text]
        detected_strengths = [kw for kw in COOPERATIVE_KEYWORDS if kw in lower_text]

        return {
            "interaction_type": interaction_type,
            "sentiment_score": round(sentiment_score, 3),
            "risk_flag_score": round(risk_flag_score, 3),
            "detected_risk_indicators": detected_flags,
            "detected_positive_indicators": detected_strengths,
            "summary_tag": "High Risk Friction" if risk_flag_score > 0.6 else ("Cooperative / Stable" if sentiment_score > 0.2 else "Moderate Neutral")
        }

    def compute_relationship_score(self, interaction_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Computes composite 0-100 relationship score from full interaction history.
        Considers recency, service failure resolution rate, and negotiation tone trajectory.
        """
        if not interaction_history:
            return {
                "relationship_score": 75.0,  # Neutral default for clean history
                "relationship_band": "neutral_untested",
                "total_interactions": 0,
                "failure_resolution_rate": 1.0,
                "sentiment_trend": "stable",
                "key_findings": ["No logged B2B friction; baseline relationship score applied."]
            }

        sentiments = []
        risk_flags = []
        failure_count = 0
        recovery_count = 0

        # Sort chronologically if dates exist
        for item in interaction_history:
            analysis = self.analyze_transcript(
                item.get("transcript_text", ""),
                item.get("interaction_type", "negotiation")
            )
            sentiments.append(analysis["sentiment_score"])
            risk_flags.append(analysis["risk_flag_score"])

            if item.get("interaction_type") == "service_failure":
                failure_count += 1
            elif item.get("interaction_type") == "service_recovery":
                recovery_count += 1

        avg_sentiment = sum(sentiments) / len(sentiments)
        avg_risk = sum(risk_flags) / len(risk_flags)
        
        # Service recovery resolution factor
        resolution_rate = (recovery_count / failure_count) if failure_count > 0 else 1.0

        # Recency weighting (latest 3 interactions carry 60% weight)
        recent_sentiments = sentiments[-3:]
        recent_sentiment = sum(recent_sentiments) / len(recent_sentiments)
        blended_sentiment = (avg_sentiment * 0.4) + (recent_sentiment * 0.6)

        # Base relationship score (0 - 100)
        # Sentiment -1.0 -> 10 pts, Sentiment 0.0 -> 65 pts, Sentiment +1.0 -> 98 pts
        raw_score = 65.0 + (blended_sentiment * 32.0) - (avg_risk * 25.0) + (resolution_rate * 5.0)
        rel_score = max(10.0, min(99.0, round(raw_score, 1)))

        findings = []
        if avg_sentiment > 0.4:
            findings.append("Positive B2B partnership tone with high cooperative consensus.")
        elif avg_sentiment < -0.2:
            findings.append("Frequent negotiation friction and recurring payment/commercial objections.")
            
        if failure_count > 0:
            if resolution_rate >= 0.8:
                findings.append(f"Strong operational resilience: {recovery_count}/{failure_count} service failures resolved successfully.")
            else:
                findings.append(f"Unresolved operational failures: {failure_count - recovery_count} incidents without confirmed recovery.")

        if rel_score >= 80:
            rel_band = "strong_partner"
        elif rel_score >= 60:
            rel_band = "stable"
        else:
            rel_band = "relationship_risk"

        return {
            "relationship_score": rel_score,
            "relationship_band": rel_band,
            "total_interactions": len(interaction_history),
            "average_sentiment": round(avg_sentiment, 3),
            "average_risk_flag": round(avg_risk, 3),
            "failure_count": failure_count,
            "recovery_count": recovery_count,
            "failure_resolution_rate": round(resolution_rate, 2),
            "key_findings": findings
        }

nlp_engine = NLPRelationshipEngine()
