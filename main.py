import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

from config.logging import setup_logging

sys.path.append(os.path.dirname(Path(__file__).parent))
import uvicorn
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pygit2 import Repository

from api.auth import get_user
from api.routes.health import router as health
from config import config, secrets

# logging
setup_logging()
logger = logging.getLogger("dataproduct")

logger.info("starting app...")

# Opt out from sending anonymous usage stats to re_data
# https://docs.getre.io/latest/docs/re_data/reference/anonymous_usage
os.environ["RE_DATA_SEND_ANONYMOUS_USAGE_STATS"] = "0"

# configuration
config = config.get_settings()
secrets.set_env_variables_from_secrets(config)

# set env for database
if not os.getenv("<PROJECT>_DB"):
    repo_name = Repository(".").head.shorthand.replace("-", "_").upper()
    if repo_name != "MAIN":
        # TODO: Bør hente ut databasenavn fra en av spesifikasjonene og ikke hardkodes
        os.environ["<PROJECT>_DB"] = repo_name + "_" + "<PROJECT>"


class IndentedJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return json.dumps(content, indent=2).encode("utf-8")


app = FastAPI(debug=True)


# static apps
app.mount(
    "/ui",
    StaticFiles(directory="apps/frontend", html=True),
    name="ui",
)

# app.mount(
#    "/dbt",
#    StaticFiles(directory="dbt/target", html=True),
#    name="dbt",
# )

# routes
app.include_router(health, tags=["health"])


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/ui")


@app.get("/error", include_in_schema=False, response_class=IndentedJSONResponse)
async def error(req: Request):
    res = {**req.headers, "cookies": {**req.cookies}, "params": {**req.path_params}}
    return res


@app.get("/logout", include_in_schema=False)
async def logout():
    RedirectResponse(url=f"/oauth2/logout/local")


@app.get("/login", include_in_schema=False)
async def logout():
    RedirectResponse(url=f"/oauth2/login")


@app.get("/user", include_in_schema=False)
async def get_user():
    user = get_user()
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@app.get("/refresh", include_in_schema=False)
async def logout():
    RedirectResponse(url=f"/oauth2/session/refresh")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
