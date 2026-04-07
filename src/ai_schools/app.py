from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ai_schools.data import CsvDistrictDataSource
from ai_schools.service import DistrictService
from ai_schools.web_api import router as api_router


def _default_data_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "districts_sample.csv"


def create_app() -> FastAPI:
    app = FastAPI(title="AI Schools", version="0.1.0")

    data_source = CsvDistrictDataSource(_default_data_path())
    service = DistrictService(data_source=data_source)
    app.state.service = service

    app.include_router(api_router)

    templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request) -> HTMLResponse:
        # Starlette's template helper signature differs across versions.
        return templates.TemplateResponse(request, "index.html", {})

    return app


app = create_app()

