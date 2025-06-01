from fastapi import APIRouter, HTTPException, Response
from typing import List, Union
from app.schemas import CommentCreate, CommentUpdate, CommentResponse, PoliteCommentResponse
from app.crud import comments

router = APIRouter()

@router.post("/",
             response_model=Union[CommentResponse, PoliteCommentResponse],
             responses={
                 200: {"model": CommentResponse},
                 201: {"model": PoliteCommentResponse}
             })
def create_comment(comment: CommentCreate, response: Response):
    data = comments.create_comment(comment)
    if data is None:
        raise HTTPException(status_code=404, detail="해당 게시글이 존재하지 않습니다.")
    
    if "polite_comment" in data:
        response.status_code = 201
        return data
    
    response.status_code = 200
    return data

@router.post("/polite", response_model=CommentResponse)
def create_comment(comment: CommentCreate):
    data = comments.create_comment(comment)
    if data is None:
        raise HTTPException(status_code=404, detail="해당 게시글이 존재하지 않습니다.")
    return data

@router.get("/{post_id}", response_model=List[CommentResponse])
def read_comments(post_id: int):
    data = comments.read_comments(post_id)
    if data is None:
        raise HTTPException(status_code=404, detail="해당 게시글이 존재하지 않습니다.")
    return data

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: int, comment: CommentUpdate):
    data = comments.update_comment(comment_id, comment)
    if data is None:
        raise HTTPException(status_code=404, detail="해당 댓글이 존재하지 않습니다.")
    return data


@router.delete("/{comment_id}")
def delete_comment(comment_id: int):
    data = comments.delete_comment(comment_id)
    if data is None:
        raise HTTPException(status_code=404, detail="해당 댓글이 존재하지 않습니다.")
    return { "message": "댓글이 삭제되었습니다."}