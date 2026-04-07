from __future__ import annotations

import pytest

from ai_schools.models import District
from ai_schools.scoring import ScoreWeights, district_score


def _district(**overrides: object) -> District:
    base = dict(
        id="x",
        name="Test District",
        state="CA",
        county="Test",
        enrollment=1000,
        student_teacher_ratio=16.0,
        graduation_rate=85.0,
        math_proficiency=50.0,
        reading_proficiency=55.0,
        per_pupil_spending=15000.0,
    )
    base.update(overrides)
    return District(**base)  # type: ignore[arg-type]


def test_district_score_is_0_100ish_and_rounded() -> None:
    s = district_score(_district())
    assert 0.0 <= s <= 100.0
    assert isinstance(s, float)
    assert round(s, 2) == s


def test_district_score_clamps_out_of_range_inputs() -> None:
    d = _district(
        graduation_rate=999,
        math_proficiency=-10,
        reading_proficiency=200,
        student_teacher_ratio=999,
        per_pupil_spending=-1,
    )
    s = district_score(d)
    assert 0.0 <= s <= 100.0


def test_district_score_rejects_negative_weights() -> None:
    d = _district()
    with pytest.raises(ValueError, match="non-negative"):
        district_score(d, ScoreWeights(graduation_rate=-0.1))


def test_district_score_rejects_zero_sum_weights() -> None:
    d = _district()
    with pytest.raises(ValueError, match="positive"):
        district_score(
            d,
            ScoreWeights(
                graduation_rate=0,
                math_proficiency=0,
                reading_proficiency=0,
                student_teacher_ratio=0,
                per_pupil_spending=0,
            ),
        )

