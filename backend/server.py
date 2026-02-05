"""
Ultra-Fast Production Server for Mendeleev Periodic Table
Optimized for 20x Performance - Fully Configurable - Bilingual
"""
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import time
import logging
import os
import sys
from pathlib import Path
import uvicorn
from database import memory_cache, connection_pool
from api import router as api_router
from security import (
    EnhancedSecurityMiddleware,
    RateLimitMiddleware,
    threat_detector
)
from database import memory_cache, connection_pool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('mendeleev_api.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration from environment variables with defaults
CONFIG = {
    "HOST": os.getenv("MENDELEEV_HOST", "127.0.0.1"),
    "PORT": int(os.getenv("MENDELEEV_PORT", "8000")),
    "WORKERS": int(os.getenv("MENDELEEV_WORKERS", "1")),
    "LOG_LEVEL": os.getenv("MENDELEEV_LOG_LEVEL", "info"),
    "RELOAD": os.getenv("MENDELEEV_RELOAD", "false").lower() == "true",
    "ACCESS_LOG": os.getenv("MENDELEEV_ACCESS_LOG", "true").lower() == "true",
    "ALLOWED_ORIGINS": os.getenv("MENDELEEV_ALLOWED_ORIGINS", "*").split(","),
    "MAX_REQUEST_SIZE": int(os.getenv("MENDELEEV_MAX_REQUEST_SIZE", "10485760")),  # 10MB
    "CORS_ENABLED": os.getenv("MENDELEEV_CORS_ENABLED", "true").lower() == "true",
    "COMPRESSION_ENABLED": os.getenv("MENDELEEV_COMPRESSION_ENABLED", "true").lower() == "true",
    "SECURITY_ENABLED": os.getenv("MENDELEEV_SECURITY_ENABLED", "true").lower() == "true",
    "RATE_LIMIT_ENABLED": os.getenv("MENDELEEV_RATE_LIMIT_ENABLED", "true").lower() == "true",
    "ENABLE_DOCS": os.getenv("MENDELEEV_ENABLE_DOCS", "true").lower() == "true",
}

def print_configuration():
    """Print server configuration"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ███╗   ███╗███████╗███╗   ██╗██████╗ ███████╗██╗       ║
║   ████╗ ████║██╔════╝████╗  ██║██╔══██╗██╔════╝██║       ║
║   ██╔████╔██║█████╗  ██╔██╗ ██║██║  ██║█████╗  ██║       ║
║   ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██║       ║
║   ██║ ╚═╝ ██║███████╗██║ ╚████║██████╔╝███████╗███████╗  ║
║   ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝  ║
║                                                          ║
║              🚀 PERIODIC TABLE API v3.0 🚀               ║
║              20x Faster | Ultra Secure | Bilingual       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """
    
    print(banner)
    print("📊 Configuration:")
    print(f"   🌐 Host: {CONFIG['HOST']}")
    print(f"   🔌 Port: {CONFIG['PORT']}")
    print(f"   👷 Workers: {CONFIG['WORKERS']}")
    print(f"   📝 Log Level: {CONFIG['LOG_LEVEL']}")
    print(f"   🔄 Reload: {CONFIG['RELOAD']}")
    print(f"   📖 Access Log: {CONFIG['ACCESS_LOG']}")
    print(f"   🌍 CORS: {CONFIG['CORS_ENABLED']}")
    print(f"   🛡️ Security: {CONFIG['SECURITY_ENABLED']}")
    print(f"   ⏱️ Rate Limit: {CONFIG['RATE_LIMIT_ENABLED']}")
    print(f"   📚 Docs: {CONFIG['ENABLE_DOCS']}")
    print(f"   💾 Max Request: {CONFIG['MAX_REQUEST_SIZE'] / 1024 / 1024:.1f}MB")
    print()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan manager for startup/shutdown events"""
    # Startup
    app.state.start_time = time.time()
    app.state.cache_hits = 0
    app.state.cache_misses = 0
    app.state.response_cache = {}
    app.state.rate_limit_logs = {}
    app.state.config = CONFIG
    
    logger.info("🚀 Mendeleev API starting up...")
    logger.info("📊 Initializing database...")
    
    from database import init_database
    init_database()
    
    yield
    
    # Shutdown
    logger.info("👋 Mendeleev API shutting down...")
    memory_cache.clear()
    connection_pool.close_all()

# Create FastAPI app with optimized settings
app_config = {
    "title": "Mendeleev Periodic Table API",
    "description": "Ultra-fast, secure, and scalable API for periodic table data - Bilingual (English/Persian)",
    "version": "3.0.0",
    "lifespan": lifespan,
}

# Conditionally include docs URLs
if CONFIG["ENABLE_DOCS"]:
    app_config.update({
        "docs_url": "/api/docs",
        "redoc_url": "/api/redoc",
        "openapi_url": "/api/openapi.json",
    })
else:
    app_config.update({
        "docs_url": None,
        "redoc_url": None,
        "openapi_url": None,
    })

app = FastAPI(**app_config)

# Add CORS middleware if enabled
if CONFIG["CORS_ENABLED"]:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CONFIG["ALLOWED_ORIGINS"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Execution-Time-MS", "X-API-Version"]
    )

# Add compression middleware if enabled
if CONFIG["COMPRESSION_ENABLED"]:
    app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add security middlewares if enabled
if CONFIG["SECURITY_ENABLED"]:
    app.add_middleware(EnhancedSecurityMiddleware)
    
if CONFIG["RATE_LIMIT_ENABLED"]:
    app.add_middleware(RateLimitMiddleware)

# Include API router
app.include_router(api_router, prefix="/api")

# Custom middleware for request logging and performance tracking
@app.middleware("http")
async def log_enhanced_requests(request: Request, call_next):
    """Middleware for request logging and performance tracking"""
    from security import log_api_request
    import time
    
    start_time = time.time()
    
    # Add request ID
    request_id = os.urandom(8).hex()
    request.state.request_id = request_id
    
    # Check request size
    if request.method in ["POST", "PUT", "PATCH"]:
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > CONFIG["MAX_REQUEST_SIZE"]:
            return JSONResponse(
                status_code=413,
                content={
                    "error": {
                        "en": "Request too large",
                        "fa": "درخواست بسیار حجیم است"
                    },
                    "max_size_mb": CONFIG["MAX_REQUEST_SIZE"] / 1024 / 1024,
                    "request_id": request_id
                }
            )
    
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request failed: {e}", exc_info=True)
        response = JSONResponse(
            status_code=500,
            content={
                "error": {
                    "en": "Internal server error",
                    "fa": "خطای داخلی سرور"
                },
                "request_id": request_id
            }
        )
    
    execution_time = (time.time() - start_time) * 1000
    
    # Log the request
    log_api_request(request, response, execution_time)
    
    # Add headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Execution-Time-MS"] = f"{execution_time:.2f}"
    response.headers["X-API-Version"] = "3.0.0"
    response.headers["X-Server-Config"] = f"host={CONFIG['HOST']},port={CONFIG['PORT']}"
    
    return response

# Root endpoint with bilingual support
@app.get("/")
async def root(request: Request, lang: str = "en"):
    """Root endpoint with system info and bilingual support"""
    # Validate language
    lang = lang if lang in ["en", "fa"] else "en"
    
    messages = {
        "en": {
            "service": "Mendeleev Periodic Table API",
            "status": "operational",
            "uptime": f"{time.time() - request.app.state.start_time:.0f} seconds",
            "endpoints": {
                "elements": "/api/elements",
                "search": "/api/search?q=hydrogen",
                "health": "/api/health",
                "stats": "/api/stats",
                "languages": "/api/languages"
            },
            "config": {
                "host": CONFIG["HOST"],
                "port": CONFIG["PORT"],
                "workers": CONFIG["WORKERS"]
            }
        },
        "fa": {
            "service": "API جدول تناوبی مندلیف",
            "status": "فعال",
            "uptime": f"{time.time() - request.app.state.start_time:.0f} ثانیه",
            "endpoints": {
                "elements": "/api/elements",
                "search": "/api/search?q=hydrogen",
                "health": "/api/health",
                "stats": "/api/stats",
                "languages": "/api/languages"
            },
            "config": {
                "host": CONFIG["HOST"],
                "port": CONFIG["PORT"],
                "workers": CONFIG["WORKERS"]
            }
        }
    }
    
    response_data = messages.get(lang, messages["en"])
    response_data["_links"] = {
        "self": "/",
        "docs": "/api/docs" if CONFIG["ENABLE_DOCS"] else None,
        "github": "https://github.com/yourusername/mendeleev-api",
        "documentation": "https://mendeleev-api.readthedocs.io"
    }
    response_data["language"] = lang
    
    return response_data

# Health endpoint
@app.get("/health")
@app.get("/سلامتی")
async def health(lang: str = "en"):
    """Simple health check with bilingual support"""
    lang = lang if lang in ["en", "fa"] else "en"
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "language": lang,
        "message": {
            "en": "API is healthy and running",
            "fa": "API سالم و در حال اجراست"
        }.get(lang)
    }

# Configuration endpoint
@app.get("/config")
async def get_configuration():
    """Get current server configuration"""
    return {
        "configuration": CONFIG,
        "environment": dict(os.environ),
        "python_version": sys.version,
        "platform": sys.platform
    }

# Serve static files for frontend
@app.get("/{path:path}")
async def serve_static(path: str):
    """Serve static files for frontend"""
    # Build path to frontend files
    project_root = Path(__file__).parent.parent
    static_paths = [
        project_root / path,
        project_root / "about" / path,
        project_root / "assets" / path,
        project_root / "more" / path,
    ]
    
    for static_path in static_paths:
        if static_path.exists() and static_path.is_file():
            # Determine content type
            content_type = "application/octet-stream"
            if path.endswith(".html"):
                content_type = "text/html; charset=utf-8"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".js"):
                content_type = "application/javascript"
            elif path.endswith(".json"):
                content_type = "application/json"
            elif path.endswith((".jpg", ".jpeg")):
                content_type = "image/jpeg"
            elif path.endswith(".png"):
                content_type = "image/png"
            elif path.endswith(".gif"):
                content_type = "image/gif"
            elif path.endswith(".svg"):
                content_type = "image/svg+xml"
            elif path.endswith(".ico"):
                content_type = "image/x-icon"
            
            from fastapi.responses import FileResponse
            return FileResponse(static_path, media_type=content_type)
    
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "en": "File not found",
                "fa": "فایل یافت نشد"
            },
            "path": path
        }
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler with bilingual support"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    # Extract request ID
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "en": "Internal server error",
                "fa": "خطای داخلی سرور"
            },
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

def run_server(host=None, port=None, workers=None, reload=None):
    """Run the server with custom configuration"""
    # Override config with provided values
    config = CONFIG.copy()
    if host:
        config["HOST"] = host
    if port:
        config["PORT"] = port
    if workers:
        config["WORKERS"] = workers
    if reload is not None:
        config["RELOAD"] = reload
    
    print_configuration()
    
    print(f"\n🚀 Starting server...")
    print(f"🌐 Access URLs:")
    print(f"   Local: http://{config['HOST']}:{config['PORT']}")
    print(f"   Network: http://<your-ip>:{config['PORT']}")
    if config["ENABLE_DOCS"]:
        print(f"📚 Documentation: http://{config['HOST']}:{config['PORT']}/api/docs")
    print(f"🔍 API Examples:")
    print(f"   Search: http://{config['HOST']}:{config['PORT']}/api/search?q=hydrogen")
    print(f"   Element: http://{config['HOST']}:{config['PORT']}/api/elements/1")
    print(f"   Stats: http://{config['HOST']}:{config['PORT']}/api/stats")
    print(f"\n⚡ Press Ctrl+C to stop\n")
    
    # Run with uvicorn
    uvicorn.run(
        "server:app",
        host=config["HOST"],
        port=config["PORT"],
        workers=config["WORKERS"],
        log_level=config["LOG_LEVEL"],
        reload=config["RELOAD"],
        access_log=config["ACCESS_LOG"],
        proxy_headers=True,
        forwarded_allow_ips="*"
    )

# Run server directly if executed
if __name__ == "__main__":
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Mendeleev Periodic Table API Server")
    parser.add_argument("--host", type=str, help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, help="Port to bind to (default: 8000)")
    parser.add_argument("--workers", type=int, help="Number of worker processes (default: 1)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    parser.add_argument("--no-docs", action="store_true", help="Disable API documentation")
    parser.add_argument("--no-cors", action="store_true", help="Disable CORS")
    parser.add_argument("--no-security", action="store_true", help="Disable security features")
    parser.add_argument("--log-level", type=str, choices=["debug", "info", "warning", "error"], help="Log level")
    
    args = parser.parse_args()
    
    # Update config based on arguments
    if args.host:
        CONFIG["HOST"] = args.host
    if args.port:
        CONFIG["PORT"] = args.port
    if args.workers:
        CONFIG["WORKERS"] = args.workers
    if args.reload:
        CONFIG["RELOAD"] = True
    if args.no_docs:
        CONFIG["ENABLE_DOCS"] = False
    if args.no_cors:
        CONFIG["CORS_ENABLED"] = False
    if args.no_security:
        CONFIG["SECURITY_ENABLED"] = False
    if args.log_level:
        CONFIG["LOG_LEVEL"] = args.log_level
    
    run_server(
        host=CONFIG["HOST"],
        port=CONFIG["PORT"],
        workers=CONFIG["WORKERS"],
        reload=CONFIG["RELOAD"]
    )