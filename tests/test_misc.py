from __future__ import annotations

import types

import pytest

import ai_schools.__main__ as main_mod
from ai_schools.data import DistrictDataSource


def test_district_datasource_base_is_abstractish() -> None:
    with pytest.raises(NotImplementedError):
        DistrictDataSource().load()


def test_cli_main_invokes_uvicorn(monkeypatch: pytest.MonkeyPatch) -> None:
    called: dict[str, object] = {}

    def fake_run(app: str, host: str, port: int, reload: bool) -> None:
        called["app"] = app
        called["host"] = host
        called["port"] = port
        called["reload"] = reload

    # Patch the imported uvicorn module inside ai_schools.__main__
    monkeypatch.setattr(main_mod, "uvicorn", types.SimpleNamespace(run=fake_run))
    monkeypatch.setenv("HOST", "0.0.0.0")
    monkeypatch.setenv("PORT", "1234")

    main_mod.main()
    assert called == {"app": "ai_schools.app:app", "host": "0.0.0.0", "port": 1234, "reload": False}

