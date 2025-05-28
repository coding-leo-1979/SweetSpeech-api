from app.database import supabase
from app.schemas import PostCreate

def create_post(post: PostCreate):
    response = supabase.table("posts").insert(post.model_dump()).execute()
    return response.data[0]

def read_posts():
    response = supabase.table("posts").select("*").execute()
    return response.data

def read_post(post_id: int):
    # post가 존재하는지 확인하기
    is_post = supabase.table("posts").select("id").eq("id", post_id).execute()
    if not is_post.data:
        return None

    response = supabase.table("posts").select("*").eq("id", post_id).execute()
    return response.data[0]

def update_post(post_id: int, post: PostCreate):
    # post가 존재하는지 확인하기
    is_post = supabase.table("posts").select("id").eq("id", post_id).execute()
    if not is_post.data:
        return None

    response = supabase.table("posts").update(post.model_dump()).eq("id", post_id).execute()
    return response.data[0]

def delete_post(post_id: int):
    # post가 존재하는지 확인하기
    is_post = supabase.table("posts").select("id").eq("id", post_id).execute()
    if not is_post.data:
        return None

    response = supabase.table("posts").delete().eq("id", post_id).execute()
    return response.data[0]