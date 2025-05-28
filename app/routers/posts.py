from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import PostCreate, PostResponse
from app.crud import posts

router = APIRouter()

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate):
    return posts.create_post(post)

@router.get("/", response_model=List[PostResponse])
def read_posts():
    return posts.read_posts()

@router.get("/{post_id}", response_model=PostResponse)
def read_post(post_id: int):
    data =  posts.read_post(post_id)
    if data is None:
        raise HTTPException(status_code=404, detail="해당 게시글이 존재하지 않습니다.")
    return data

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostCreate):
    data =  posts.update_post(post_id, post)
    if data is None:
        raise HTTPException(status_code=404, detail="해당 게시글이 존재하지 않습니다.")
    return data

@router.delete("/{post_id}")
def delete_post(post_id: int):
    data =  posts.delete_post(post_id)
    if data is None:
        raise HTTPException(status_code=404, detail="해당 게시글이 존재하지 않습니다.")
    return { "message": "게시글이 삭제되었습니다."}