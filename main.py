from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import router as api_router

app = FastAPI()

# ✅ CORS for HTTP routes (safe for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only. Use specific domains in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include all endpoints and WebSocket routes
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
