from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from app.routers import auth, bots, groups
except ImportError:
    from routers import auth, bots, groups

app = FastAPI()


origins = [
    "*",  # Allow all origins
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    'https://9sv4psq6-5000.euw.devtunnels.ms'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router for authentication
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include the router for bot management
app.include_router(bots.router, prefix="/bots", tags=["bot"])

# Include the router for group management
app.include_router(groups.router, prefix="/groups", tags=["groups"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
