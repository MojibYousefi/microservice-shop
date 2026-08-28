import httpx
from typing import Optional, Dict, Any, Set, AsyncGenerator
from fastapi import Request, Response, HTTPException, status
from backend.config.config import settings


class NetworkManager:
    """
    Manages internal network communication, connection pooling, and request proxying
    between the API Gateway and internal microservices.
    """

    def __init__(self, timeout: float = 30.0) -> None:
        self.timeout = timeout
        self.client: Optional[httpx.AsyncClient] = None

    async def start(self) -> None:
        """
        Initializes the async HTTP connection pool for internal network communication.
        """
        if self.client is None or self.client.is_closed:
            self.client = httpx.AsyncClient(timeout=self.timeout)

    async def stop(self) -> None:
        """
        Closes internal network HTTP client connections.
        """
        if self.client is not None and not self.client.is_closed:
            await self.client.aclose()
            self.client = None

    async def forward_request(self, request: Request, target_service_url: str) -> Response:
        """
        Asynchronously proxies and forwards incoming HTTP requests from Gateway to internal microservices.
        Ensures all client communication passes through the Gateway entrypoint.
        """
        if self.client is None or self.client.is_closed:
            await self.start()

        client = self.client
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Internal network client is unavailable."
            )

        url_path = request.url.path
        query_string = request.url.query
        target_url = f"{target_service_url}{url_path}"
        if query_string:
            target_url = f"{target_url}?{query_string}"

        # Clean headers & prepare internal routing headers
        headers = dict(request.headers)
        headers.pop("host", None)
        headers["X-Forwarded-Host"] = request.headers.get("host", "")
        headers["X-Forwarded-Proto"] = request.url.scheme

        body = await request.body()

        try:
            req = client.build_request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body
            )
            res = await client.send(req, stream=True)

            excluded_headers: Set[str] = {
                "content-encoding",
                "content-length",
                "transfer-encoding",
                "connection"
            }
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
                detail=f"Internal network proxy error to {target_service_url}: {str(exc)}"
            )

    async def check_health(self, service_map: Dict[str, str]) -> Dict[str, str]:
        """
        Inspects internal microservices health reachability.
        """
        statuses: Dict[str, str] = {}
        for service_name, service_url in service_map.items():
            try:
                if self.client is not None and not self.client.is_closed:
                    resp = await self.client.get(f"{service_url}/health", timeout=3.0)
                else:
                    async with httpx.AsyncClient(timeout=3.0) as temp_client:
                        resp = await temp_client.get(f"{service_url}/health")

                if resp.status_code == 200:
                    statuses[service_name] = "healthy"
                else:
                    statuses[service_name] = f"unhealthy (status {resp.status_code})"
            except Exception as e:
                statuses[service_name] = f"unreachable ({str(e)})"
        return statuses


# Global network manager instance
network_manager = NetworkManager()


async def get_network_manager() -> AsyncGenerator[NetworkManager, None]:
    """
    FastAPI dependency for accessing the NetworkManager.
    """
    yield network_manager

