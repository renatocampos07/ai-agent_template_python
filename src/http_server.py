import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Dict
from urllib.parse import parse_qs, urlparse

from .data_loader import chunk_documents, load_documents
from .handler import handler, warmup
from .llm_provider import get_embeddings, get_settings
from .vector_store import build_vector_store, persist_vector_store


def _str_to_bool(value: str) -> bool:
    return value.lower() in {"1", "true", "t", "yes", "y"}


def _bootstrap_vector_store() -> None:
    settings = get_settings()
    target_dir = Path(settings.vector_store_path)

    if target_dir.exists():
        return

    auto_build = _str_to_bool(os.getenv("AUTO_BUILD_VECTOR_STORE", "false"))
    if not auto_build:
        raise FileNotFoundError(
            f"Vector store não encontrado em '{target_dir}'. Execute 'python vetorize.py' antes do deploy ou defina AUTO_BUILD_VECTOR_STORE=true."
        )

    documents = load_documents(Path(settings.rag_data_path))
    chunks = chunk_documents(documents)
    embeddings = get_embeddings()
    store = build_vector_store(chunks, embeddings)
    persist_vector_store(store, target_dir)


class AgentRequestHandler(BaseHTTPRequestHandler):
    server_version = "AgentHTTP/0.1"

    def log_message(self, format: str, *args) -> None:  # noqa: D401 - reduz verbosidade
        os.environ.get("LOG_HTTP", "false").lower() in {"1", "true"} and super().log_message(format, *args)

    def _write_response(self, status_code: int, body: str, headers: Dict[str, str] | None = None) -> None:
        payload = body.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        if headers:
            for key, value in headers.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802 - assinatura da classe base
        parsed = urlparse(self.path)
        if parsed.path in {"/", ""}:
            message = json.dumps(
                {
                    "message": "Use POST /query com JSON {'question': '...'} ou GET /health",
                    "endpoints": {
                        "health": "/health",
                        "query": "/query",
                    },
                }
            )
            self._write_response(200, message)
            return

        if parsed.path == "/health":
            self._write_response(200, json.dumps({"status": "ok"}))
            return

        if parsed.path == "/query":
            params = parse_qs(parsed.query)
            question = params.get("question", [None])[0]
            if not question:
                self._write_response(400, json.dumps({"error": "Informe 'question' na query string."}))
                return
            event = {
                "question": question,
                "httpMethod": "GET",
                "path": parsed.path,
                "queryStringParameters": {k: v[0] for k, v in params.items()},
            }
            response = handler(event)
            self._write_response(response.get("statusCode", 500), response.get("body", "{}"))
            return

        self._write_response(404, json.dumps({"error": "Endpoint não encontrado."}))

    def do_POST(self) -> None:  # noqa: N802 - assinatura da classe base
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b""
        body_str = raw_body.decode("utf-8")

        event = {
            "body": body_str,
            "headers": dict(self.headers),
            "httpMethod": "POST",
            "path": parsed.path,
        }

        if parsed.query:
            params = {k: v[0] for k, v in parse_qs(parsed.query).items()}
            event["queryStringParameters"] = params
            if "question" in params and not body_str:
                event["question"] = params["question"]

        response = handler(event)
        self._write_response(response.get("statusCode", 500), response.get("body", "{}"))


def run_server() -> None:
    host = os.getenv("AGENT_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("AGENT_SERVER_PORT", "8000"))
    server = HTTPServer((host, port), AgentRequestHandler)
    print(f"Servidor iniciado em http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    try:
        _bootstrap_vector_store()
        warmup()
    except FileNotFoundError as exc:
        print(
            "Vector store ausente e AUTO_BUILD_VECTOR_STORE desativado."
            " Execute 'python vetorize.py' ou defina AUTO_BUILD_VECTOR_STORE=true."
        )
        raise SystemExit(str(exc))
    run_server()
