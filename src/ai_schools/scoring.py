from __future__ import annotations

from dataclasses import dataclass

from ai_schools.models import District


@dataclass(frozen=True, slots=True)
class ScoreWeights:
    graduation_rate: float = 0.30
    math_proficiency: float = 0.20
    reading_proficiency: float = 0.20
    student_teacher_ratio: float = 0.15  # lower is better
    per_pupil_spending: float = 0.15


def _clamp(value: float, lo: float, hi: float) -> float:
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


def _normalize_0_100(value: float) -> float:
    return _clamp(value, 0.0, 100.0)


def _normalize_ratio(ratio: float) -> float:
    """
    Convert student-teacher ratio (lower better) into a 0..100 score.
    10:1 -> 100, 25:1 -> 0, linearly interpolated and clamped.
    """
    ratio = _clamp(ratio, 10.0, 25.0)
    return (25.0 - ratio) / (25.0 - 10.0) * 100.0


def _normalize_spending(spending: float) -> float:
    """
    Convert per-pupil spending into a 0..100 score.
    $8k -> 0, $25k -> 100, linearly interpolated and clamped.
    """
    spending = _clamp(spending, 8000.0, 25000.0)
    return (spending - 8000.0) / (25000.0 - 8000.0) * 100.0


def _validate_weights(weights: ScoreWeights) -> None:
    fields = (
        weights.graduation_rate,
        weights.math_proficiency,
        weights.reading_proficiency,
        weights.student_teacher_ratio,
        weights.per_pupil_spending,
    )
    if any(w < 0 for w in fields):
        raise ValueError("weights must be non-negative")
    total = sum(fields)
    if total <= 0:
        raise ValueError("weights must sum to a positive number")


def district_score(d: District, weights: ScoreWeights | None = None) -> float:
    """
    Weighted 0..100 district score (higher is better).
    """
    weights = weights or ScoreWeights()
    _validate_weights(weights)

    g = _normalize_0_100(d.graduation_rate)
    m = _normalize_0_100(d.math_proficiency)
    r = _normalize_0_100(d.reading_proficiency)
    str_score = _normalize_ratio(d.student_teacher_ratio)
    spend_score = _normalize_spending(d.per_pupil_spending)

    total_w = (
        weights.graduation_rate
        + weights.math_proficiency
        + weights.reading_proficiency
        + weights.student_teacher_ratio
        + weights.per_pupil_spending
    )
    score = (
        g * weights.graduation_rate
        + m * weights.math_proficiency
        + r * weights.reading_proficiency
        + str_score * weights.student_teacher_ratio
        + spend_score * weights.per_pupil_spending
    ) / total_w
    return round(float(score), 2)

