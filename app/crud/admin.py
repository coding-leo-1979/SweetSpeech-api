from app.database import supabase
from app.schemas import CommentCreate, CommentUpdate

def read_comments_need_review():
    response = supabase.table("comments").select("*").eq("needs_review", "true").order("id").execute()
    return response.data

def read_comment_post(comment_id: int):
    # 댓글 조회하기
    response_comment = supabase.table("comments").select("*").eq("id", comment_id).execute()
    comment = response_comment.data[0]

    # 댓글이 달린 게시글 조회하기
    response_post = supabase.table("posts").select("*").eq("id", comment["post_id"]).execute()
    post = response_post.data[0]

    return post

def comment_is_not_bad(comment_id: int):
    # needs_review를 True에서 False로 업데이트
    response = supabase.table("comments") \
                .update({"needs_review": "false"}) \
                .eq("id", comment_id).execute()
    return response.data[0]

def comment_is_bad(comment_id: int):
    # comment가 존재하는지 확인하기
    is_comment = supabase.table("comments").select("id").eq("id", comment_id).execute()
    if not is_comment.data:
        return None
    
    response = supabase.table("comments").delete().eq("id", comment_id).execute()
    return response.data[0]

def comment_block(comment_id: int, comment: CommentUpdate):
    # comment가 존재하는지 확인하기
    is_comment = supabase.table("comments").select("id").eq("id", comment_id).execute()
    if not is_comment.data:
        return None
    
    update_data = comment.model_dump()

    reason = comment.content or "관리자 판단"
    update_data['content'] = f"블락된 댓글입니다. (사유: {reason})"
    update_data['needs_review'] = "blocked"

    response = supabase.table("comments").update(update_data).eq("id", comment_id).execute()
    return response.data[0]