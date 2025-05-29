from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import PostResponse, CommentCreate, CommentResponse
from app.crud import admin

router = APIRouter()

@router.get("/", response_model=List[CommentResponse])
def read_comments_need_review():
    return admin.read_comments_need_review()

@router.get("/{comment_id}", response_model=PostResponse)
def read_comment_post(comment_id: int):
    post = admin.read_comment_post(comment_id)
    if post is None:
        raise HTTPException(status_code=404, detail="해당 게시글이 존재하지 않습니다.")
    return post

@router.put("/{comment_id}", response_model=CommentResponse)
def comment_is_not_bad(comment_id: int):
    updated_comment = admin.comment_is_not_bad(comment_id)
    if updated_comment is None:
        raise HTTPException(status_code=404, detail="해당 댓글을 찾을 수 없습니다.")
    return updated_comment

@router.delete("/{comment_id}")
def delete_comment(comment_id: int):
    data = admin.comment_is_bad(comment_id)
    if data is None:
        raise HTTPException(status_code=404, detail="해당 댓글이 존재하지 않습니다.")
    return { "message": "댓글이 삭제되었습니다."}