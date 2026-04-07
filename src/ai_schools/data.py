from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from ai_schools.models import District


class DistrictDataSource:
    def load(self) -> list[District]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class CsvDistrictDataSource(DistrictDataSource):
    path: Path

    def load(self) -> list[District]:
        if not self.path.exists():
            raise FileNotFoundError(str(self.path))

        with self.path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            districts: list[District] = []
            for row in reader:
                districts.append(
                    District(
                        id=row["id"].strip(),
                        name=row["name"].strip(),
                        state=row["state"].strip(),
                        county=row["county"].strip(),
                        enrollment=int(row["enrollment"]),
                        student_teacher_ratio=float(row["student_teacher_ratio"]),
                        graduation_rate=float(row["graduation_rate"]),
                        math_proficiency=float(row["math_proficiency"]),
                        reading_proficiency=float(row["reading_proficiency"]),
                        per_pupil_spending=float(row["per_pupil_spending"]),
                    )
                )
        return districts

