from __future__ import annotations

import os

import uvicorn


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("ai_schools.app:app", host=host, port=port, reload=False)


if __name__ == "__main__":  # pragma: no cover
    main()

