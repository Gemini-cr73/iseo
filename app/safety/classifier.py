import re

from app.safety.schemas import SafetySignal

PATTERNS: dict[str, list[tuple[str, float, str]]] = {
    "cyber": [
        (
            r"\b(phish|phishing|malware|ransomware|exploit|payload|keylogger)\b",
            0.95,
            "Potential cyber abuse request.",
        ),
        (
            r"\b(hack|breach|ddos|botnet|credential stuffing|unauthorized access)\b",
            0.9,
            "Potential unauthorized cyber activity.",
        ),
        (
            r"\b(bypass|bypass security|bypass security systems|disable security|evade detection|break into|crack password|steal passwords)\b",
            0.92,
            "Potential request to bypass or defeat security controls.",
        ),
    ],
    "privacy": [
        (
            r"\b(ssn|social security|passport number|credit card|cvv)\b",
            0.9,
            "Sensitive personal data detected.",
        ),
        (
            r"\b(doxx|doxing|leak personal info)\b",
            0.95,
            "Possible privacy harm or exposure.",
        ),
    ],
    "medical": [
        (
            r"\b(diagnose|prescribe|dosage|treatment plan)\b",
            0.75,
            "Medical guidance request may need caution.",
        ),
    ],
    "financial": [
        (
            r"\b(insider trading|pump and dump|guaranteed profit)\b",
            0.85,
            "Potential harmful financial guidance.",
        ),
    ],
    "violence": [
        (
            r"\b(build a bomb|make explosives|poison someone|kill)\b",
            1.0,
            "Violent or dangerous request.",
        ),
    ],
    "legal": [
        (
            r"\b(evade taxes|forge document|fake id|counterfeit)\b",
            0.9,
            "Potential illegal activity request.",
        ),
    ],
}

RISKY_PHRASES: list[tuple[str, str, float, str]] = [
    (
        "cyber",
        "bypass security systems",
        0.95,
        "Potential request to defeat security protections.",
    ),
    (
        "cyber",
        "bypass security",
        0.92,
        "Potential request to defeat security protections.",
    ),
    (
        "cyber",
        "how to bypass",
        0.88,
        "Potential request for evasion or unauthorized access guidance.",
    ),
    (
        "cyber",
        "disable security",
        0.9,
        "Potential request to weaken or disable protection systems.",
    ),
    (
        "cyber",
        "steal passwords",
        0.98,
        "Potential credential theft request.",
    ),
    (
        "cyber",
        "break into",
        0.9,
        "Potential unauthorized access request.",
    ),
    (
        "cyber",
        "evade detection",
        0.9,
        "Potential request to avoid security monitoring.",
    ),
]

SAFE_CONTEXT_HINTS = [
    "prevent",
    "defend",
    "protect",
    "mitigate",
    "detect",
    "awareness",
    "training",
    "security policy",
    "best practices",
    "how to stop",
    "how to prevent",
]


def _dedupe_signals(signals: list[SafetySignal]) -> list[SafetySignal]:
    seen: set[tuple[str, str, str]] = set()
    unique: list[SafetySignal] = []

    for signal in signals:
        key = (
            signal.category,
            signal.matched_text.lower(),
            signal.rationale,
        )
        if key not in seen:
            seen.add(key)
            unique.append(signal)

    return unique


def _is_probably_defensive_request(text: str) -> bool:
    lowered = text.lower()
    return any(hint in lowered for hint in SAFE_CONTEXT_HINTS)


def classify_safety_signals(text: str) -> list[SafetySignal]:
    clean_text = text.strip()
    lowered = clean_text.lower()

    signals: list[SafetySignal] = []

    # Direct phrase matching first for stronger intent capture
    for category, phrase, severity, rationale in RISKY_PHRASES:
        if phrase in lowered:
            signals.append(
                SafetySignal(
                    category=category,
                    matched_text=phrase,
                    severity=severity,
                    rationale=rationale,
                )
            )

    # Regex pattern matching
    for category, rules in PATTERNS.items():
        for pattern, severity, rationale in rules:
            match = re.search(pattern, lowered)
            if match:
                signals.append(
                    SafetySignal(
                        category=category,
                        matched_text=match.group(0),
                        severity=severity,
                        rationale=rationale,
                    )
                )

    # Reduce severity slightly for clearly defensive contexts
    if signals and _is_probably_defensive_request(clean_text):
        adjusted: list[SafetySignal] = []
        for signal in signals:
            adjusted.append(
                SafetySignal(
                    category=signal.category,
                    matched_text=signal.matched_text,
                    severity=max(0.35, round(signal.severity - 0.2, 2)),
                    rationale=f"{signal.rationale} Defensive context detected; severity reduced.",
                )
            )
        signals = adjusted

    return _dedupe_signals(signals)
