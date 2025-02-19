# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import resume_routes, question_routes, evaluation_routes, proctor_routes
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="AI Interview Chatbot API",
    description="API for AI-powered interview chatbot",
    version="1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume_routes.router, prefix="/api")
app.include_router(question_routes.router, prefix="/api")
app.include_router(evaluation_routes.router, prefix="/api")
app.include_router(proctor_routes.router, prefix="/api")

@app.get("/")
async def root():
    """Redirect root to docs"""
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001) 