from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class District:
    id: str
    name: str
    state: str
    county: str
    enrollment: int
    student_teacher_ratio: float
    graduation_rate: float  # 0..100
    math_proficiency: float  # 0..100
    reading_proficiency: float  # 0..100
    per_pupil_spending: float  # USD

