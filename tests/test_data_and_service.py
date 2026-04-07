from __future__ import annotations

from pathlib import Path

import pytest

from ai_schools.data import CsvDistrictDataSource, DistrictDataSource
from ai_schools.models import District
from ai_schools.service import DistrictService


class _MemorySource(DistrictDataSource):
    def __init__(self, districts: list[District]) -> None:
        self._districts = districts
        self.calls = 0

    def load(self) -> list[District]:
        self.calls += 1
        return list(self._districts)


def test_csv_datasource_loads_expected_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "d.csv"
    csv_path.write_text(
        "id,name,state,county,enrollment,student_teacher_ratio,graduation_rate,math_proficiency,reading_proficiency,per_pupil_spending\n"
        "1,A,CA,X,10,15.0,90,60,70,12000\n",
        encoding="utf-8",
    )
    ds = CsvDistrictDataSource(csv_path)
    districts = ds.load()
    assert districts[0].name == "A"
    assert districts[0].enrollment == 10


def test_csv_datasource_missing_file_raises(tmp_path: Path) -> None:
    ds = CsvDistrictDataSource(tmp_path / "missing.csv")
    with pytest.raises(FileNotFoundError):
        ds.load()


def test_service_caches_load() -> None:
    d = District(
        id="1",
        name="A",
        state="CA",
        county="X",
        enrollment=10,
        student_teacher_ratio=15.0,
        graduation_rate=90.0,
        math_proficiency=60.0,
        reading_proficiency=70.0,
        per_pupil_spending=12000.0,
    )
    src = _MemorySource([d])
    svc = DistrictService(src)
    assert svc.get("1") is not None
    assert svc.list()
    assert src.calls == 1


def test_service_search_filters_and_paginates() -> None:
    districts = [
        District(
            id="1",
            name="Alpha",
            state="CA",
            county="Orange",
            enrollment=100,
            student_teacher_ratio=16.0,
            graduation_rate=80.0,
            math_proficiency=50.0,
            reading_proficiency=55.0,
            per_pupil_spending=15000.0,
        ),
        District(
            id="2",
            name="Beta",
            state="NY",
            county="Kings",
            enrollment=200,
            student_teacher_ratio=16.0,
            graduation_rate=80.0,
            math_proficiency=50.0,
            reading_proficiency=55.0,
            per_pupil_spending=15000.0,
        ),
        District(
            id="3",
            name="Gamma",
            state="CA",
            county="Kings",
            enrollment=300,
            student_teacher_ratio=16.0,
            graduation_rate=80.0,
            math_proficiency=50.0,
            reading_proficiency=55.0,
            per_pupil_spending=15000.0,
        ),
    ]
    svc = DistrictService(_MemorySource(districts))
    assert [d.id for d in svc.search(state="CA")] == ["1", "3"]
    assert [d.id for d in svc.search(q="king")] == ["2", "3"]
    assert [d.id for d in svc.search(min_enrollment=150)] == ["2", "3"]
    assert [d.id for d in svc.search(max_enrollment=150)] == ["1"]
    assert [d.id for d in svc.search(limit=1, offset=1)] == ["2"]


def test_service_search_rejects_bad_pagination() -> None:
    svc = DistrictService(_MemorySource([]))
    with pytest.raises(ValueError):
        svc.search(limit=0)
    with pytest.raises(ValueError):
        svc.search(limit=201)
    with pytest.raises(ValueError):
        svc.search(offset=-1)


def test_service_top_sorts_and_filters() -> None:
    d1 = District(
        id="1",
        name="A",
        state="CA",
        county="X",
        enrollment=10,
        student_teacher_ratio=25.0,
        graduation_rate=50.0,
        math_proficiency=50.0,
        reading_proficiency=50.0,
        per_pupil_spending=8000.0,
    )
    d2 = District(
        id="2",
        name="B",
        state="CA",
        county="Y",
        enrollment=10,
        student_teacher_ratio=10.0,
        graduation_rate=99.0,
        math_proficiency=80.0,
        reading_proficiency=70.0,
        per_pupil_spending=25000.0,
    )
    svc = DistrictService(_MemorySource([d1, d2]))
    top = svc.top(n=1)
    assert top[0].district.id == "2"
    assert svc.top(n=10, state="CA")


def test_service_top_rejects_bad_n() -> None:
    svc = DistrictService(_MemorySource([]))
    with pytest.raises(ValueError):
        svc.top(n=0)
    with pytest.raises(ValueError):
        svc.top(n=201)

