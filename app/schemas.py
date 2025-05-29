from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class PostResponse(PostCreate):
    id: int
    created_at: str
    updated_at: str
    likes: int = 0
    comment_count: int = 0

class CommentCreate(BaseModel):
    post_id: int
    content: str

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(CommentCreate):
    id: int
    created_at: str
    updated_at: str

class SanitizedCommentResponse(BaseModel):
    sanitized_comment: str