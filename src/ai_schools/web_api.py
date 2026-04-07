from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from ai_schools.scoring import ScoreWeights, district_score
from ai_schools.service import DistrictService

router = APIRouter(prefix="/api")


def _service(request: Request) -> DistrictService:
    return request.app.state.service


class DistrictOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    state: str
    county: str
    enrollment: int
    student_teacher_ratio: float
    graduation_rate: float
    math_proficiency: float
    reading_proficiency: float
    per_pupil_spending: float


class ScoredDistrictOut(BaseModel):
    district: DistrictOut
    score: float


class ScoreWeightsIn(BaseModel):
    graduation_rate: float = Field(default=0.30, ge=0)
    math_proficiency: float = Field(default=0.20, ge=0)
    reading_proficiency: float = Field(default=0.20, ge=0)
    student_teacher_ratio: float = Field(default=0.15, ge=0)
    per_pupil_spending: float = Field(default=0.15, ge=0)

    def to_weights(self) -> ScoreWeights:
        return ScoreWeights(
            graduation_rate=self.graduation_rate,
            math_proficiency=self.math_proficiency,
            reading_proficiency=self.reading_proficiency,
            student_teacher_ratio=self.student_teacher_ratio,
            per_pupil_spending=self.per_pupil_spending,
        )


class TopRequest(BaseModel):
    n: int = Field(default=10, ge=1, le=200)
    state: str | None = None
    weights: ScoreWeightsIn | None = None


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/districts", response_model=list[DistrictOut])
def list_districts(
    request: Request,
    q: str | None = None,
    state: str | None = None,
    min_enrollment: int | None = None,
    max_enrollment: int | None = None,
    limit: int = 25,
    offset: int = 0,
) -> list[DistrictOut]:
    svc = _service(request)
    try:
        districts = svc.search(
            q=q,
            state=state,
            min_enrollment=min_enrollment,
            max_enrollment=max_enrollment,
            limit=limit,
            offset=offset,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return [DistrictOut.model_validate(d) for d in districts]


@router.get("/districts/{district_id}", response_model=DistrictOut)
def get_district(request: Request, district_id: str) -> DistrictOut:
    svc = _service(request)
    d = svc.get(district_id)
    if d is None:
        raise HTTPException(status_code=404, detail="district not found")
    return DistrictOut.model_validate(d)


@router.post("/top", response_model=list[ScoredDistrictOut])
def top_districts(request: Request, payload: TopRequest) -> list[ScoredDistrictOut]:
    svc = _service(request)
    weights = payload.weights.to_weights() if payload.weights else None
    scored = svc.top(n=payload.n, weights=weights, state=payload.state)

    return [
        ScoredDistrictOut(
            district=DistrictOut.model_validate(sd.district),
            score=sd.score,
        )
        for sd in scored
    ]


@router.get("/districts/{district_id}/score")
def score_district(request: Request, district_id: str) -> dict[str, float]:
    svc = _service(request)
    d = svc.get(district_id)
    if d is None:
        raise HTTPException(status_code=404, detail="district not found")
    return {"score": district_score(d)}

