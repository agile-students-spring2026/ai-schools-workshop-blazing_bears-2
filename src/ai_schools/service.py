from __future__ import annotations

from dataclasses import dataclass

from ai_schools.data import DistrictDataSource
from ai_schools.models import District
from ai_schools.scoring import ScoreWeights, district_score


@dataclass(frozen=True, slots=True)
class ScoredDistrict:
    district: District
    score: float


class DistrictService:
    def __init__(self, data_source: DistrictDataSource) -> None:
        self._data_source = data_source
        self._districts: list[District] | None = None

    def _ensure_loaded(self) -> list[District]:
        if self._districts is None:
            self._districts = self._data_source.load()
        return self._districts

    def list(self) -> list[District]:
        return list(self._ensure_loaded())

    def get(self, district_id: str) -> District | None:
        district_id = district_id.strip()
        for d in self._ensure_loaded():
            if d.id == district_id:
                return d
        return None

    def search(
        self,
        *,
        q: str | None = None,
        state: str | None = None,
        min_enrollment: int | None = None,
        max_enrollment: int | None = None,
        limit: int = 25,
        offset: int = 0,
    ) -> list[District]:
        if limit < 1 or limit > 200:
            raise ValueError("limit must be between 1 and 200")
        if offset < 0:
            raise ValueError("offset must be >= 0")

        q_norm = (q or "").strip().lower()
        state_norm = (state or "").strip().upper()

        results: list[District] = []
        for d in self._ensure_loaded():
            if state_norm and d.state.upper() != state_norm:
                continue
            if min_enrollment is not None and d.enrollment < min_enrollment:
                continue
            if max_enrollment is not None and d.enrollment > max_enrollment:
                continue
            if q_norm and q_norm not in d.name.lower() and q_norm not in d.county.lower():
                continue
            results.append(d)

        return results[offset : offset + limit]

    def top(
        self,
        *,
        n: int = 10,
        weights: ScoreWeights | None = None,
        state: str | None = None,
    ) -> list[ScoredDistrict]:
        if n < 1 or n > 200:
            raise ValueError("n must be between 1 and 200")
        weights = weights or ScoreWeights()
        state_norm = (state or "").strip().upper()

        scored: list[ScoredDistrict] = []
        for d in self._ensure_loaded():
            if state_norm and d.state.upper() != state_norm:
                continue
            scored.append(ScoredDistrict(district=d, score=district_score(d, weights)))
        scored.sort(key=lambda sd: sd.score, reverse=True)
        return scored[:n]

