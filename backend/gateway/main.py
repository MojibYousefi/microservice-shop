import os
import sys
from typing import Optional, AsyncGenerator, Dict, Any, Set
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.config.config import settings

# Global async HTTP client for proxying requests
http_client: Optional[httpx.AsyncClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global http_client
    http_client = httpx.AsyncClient(timeout=30.0)
    try:
        yield
    finally:
        if http_client is not None:
            await http_client.aclose()


app = FastAPI(
    title=f"{settings.PROJECT_NAME} - API Gateway (XHTTP)",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def gateway_health() -> Dict[str, Any]:
    """
    Health check verifying Gateway and internal service reachability.
    """
    services_status: Dict[str, str] = {}
    service_map: Dict[str, str] = {
        "auth_service": settings.AUTH_SERVICE_URL,
    }

    for service_name, service_url in service_map.items():
        try:
            if http_client is not None:
                resp = await http_client.get(f"{service_url}/health", timeout=3.0)
                if resp.status_code == 200:
                    services_status[service_name] = "healthy"
                else:
                    services_status[service_name] = f"unhealthy (status {resp.status_code})"
            else:
                async with httpx.AsyncClient(timeout=3.0) as temp_client:
                    resp = await temp_client.get(f"{service_url}/health")
                    if resp.status_code == 200:
                        services_status[service_name] = "healthy"
                    else:
                        services_status[service_name] = f"unhealthy (status {resp.status_code})"
        except Exception as e:
            services_status[service_name] = f"unreachable ({str(e)})"

    return {
        "gateway": "healthy",
        "debug_mode": settings.DEBUG,
        "services": services_status
    }


async def forward_request(request: Request, target_service_url: str) -> Response:
    """
    Asynchronous XHTTP request proxying and forwarding mechanism.
    Routes request method, headers, query parameters, and body to internal microservices.
    """
    url_path = request.url.path
    query_string = request.url.query
    target_url = f"{target_service_url}{url_path}"
    if query_string:
        target_url = f"{target_url}?{query_string}"

    headers = dict(request.headers)
    headers.pop("host", None)

    # Read body asynchronously
    body = await request.body()

    client = http_client
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="HTTP proxy client is uninitialized."
        )

    try:
        req = client.build_request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body
        )
        res = await client.send(req, stream=True)

        excluded_headers: Set[str] = {"content-encoding", "content-length", "transfer-encoding", "connection"}
        response_headers = {
            k: v for k, v in res.headers.items() if k.lower() not in excluded_headers
        }

        return Response(
            content=await res.aread(),
            status_code=res.status_code,
            headers=response_headers
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service proxy error to {target_service_url}: {str(exc)}"
        )


# ==========================================
# Route Handlers for Gateway
# ==========================================

@app.api_route("/api/v1/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
async def route_auth(request: Request, path: str) -> Response:
    return await forward_request(request, settings.AUTH_SERVICE_URL)


@app.api_route("/api/v1/auth", methods=["GET", "POST", "OPTIONS"])
async def route_auth_root(request: Request) -> Response:
    return await forward_request(request, settings.AUTH_SERVICE_URL)


# Mount frontend static directory if exists
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
if os.path.exists(frontend_dir):
    app.mount("/shop", StaticFiles(directory=frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.GATEWAY_PORT)
