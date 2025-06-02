from app.database import supabase
from app.schemas import CommentCreate, CommentUpdate
from app.middlewares.openai_model import polite_comment_middleware
from app.middlewares.classification_model import is_impolite_middleware

def create_comment(comment: CommentCreate):
    # post가 존재하는지 확인하기
    is_post = supabase.table("posts").select("id").eq("id", comment.post_id).execute()
    if not is_post.data:
        return None

    # 악플 여부
    is_impolite, needs_review = is_impolite_middleware(comment.content)
    
    # 악플인 경우
    if is_impolite:
        polite_comment = polite_comment_middleware(comment.content)
        comment.content = polite_comment
        return { "polite_comment": polite_comment }

    # 악플이 아닌 경우
    else:
        comment_data = comment.model_dump()
        comment_data["needs_review"] = needs_review

        response = supabase.table("comments").insert(comment_data).execute()
        return response.data[0]

def create_polite_comment(comment: CommentCreate):
    # post가 존재하는지 확인하기
    is_post = supabase.table("posts").select("id").eq("id", comment.post_id).execute()
    if not is_post.data:
        return None
    
    response = supabase.table("comments").insert(comment.model_dump()).execute()
    return response.data[0]


def read_comments(post_id: int):
    # post가 존재하는지 확인하기
    is_post = supabase.table("posts").select("id").eq("id", post_id).execute()
    if not is_post.data:
        return None
    
    response = supabase.table("comments").select("*").eq("post_id", post_id).order("id").execute()
    comments = response.data

    # 관리자가 검토 중인 댓글인지 확인하기
    for comment in comments:
        if comment.get("needs_review", True):
            comment["content"] = "관리자가 검토 중인 댓글입니다."

    return comments

def update_comment(comment_id: int, comment: CommentUpdate):
    # comment가 존재하는지 확인하기
    is_comment = supabase.table("comments").select("id").eq("id", comment_id).execute()
    if not is_comment.data:
        return None

    response = supabase.table("comments").update(comment.model_dump()).eq("id", comment_id).execute()
    return response.data[0]

def delete_comment(comment_id: int):
    # comment가 존재하는지 확인하기
    is_comment = supabase.table("comments").select("id").eq("id", comment_id).execute()
    if not is_comment.data:
        return None
    
    response = supabase.table("comments").delete().eq("id", comment_id).execute()
    return response.data[0]