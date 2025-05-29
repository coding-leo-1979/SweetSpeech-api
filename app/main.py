from fastapi import FastAPI
from app.routers import posts, comments, admin

app = FastAPI()

app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
