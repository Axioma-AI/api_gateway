# from src.dependencies.auth import require_token
# from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
# from typing import Optional, List
# from src.services.auth_service import AuthService
# from src.services.axioma_service import AxiomaService
# from src.schema.responses import ArticleResponse, SourceResponse, UserResponse

# router = APIRouter(prefix="/gateway")

# auth_service = AuthService()
# axioma_service = AxiomaService()

# @router.get("/articles")
# async def articles(
#     page: int = Query(1, ge=1),
#     start_date: Optional[str] = Query(None),
#     end_date: Optional[str] = Query(None),
# ):
#     return await axioma_service.get_articles(
#         page=page, start_date=start_date, end_date=end_date
#     )

# @router.get("/articles/search")
# async def search_articles(
#     query: str,
#     page: int = Query(1, ge=1),
#     start_date: Optional[str] = Query(None),
#     end_date: Optional[str] = Query(None),
# ):
#     return await axioma_service.search_articles(
#         token,
#         query,
#         page=page,
#         start_date=start_date,
#         end_date=end_date,
#     )

# @router.get("/articles/pages")
# async def article_pages(
#     start_date: Optional[str] = Query(None),
#     end_date: Optional[str] = Query(None),
# ):
#     return await axioma_service.get_article_pages(
#         token, start_date=start_date, end_date=end_date
#     )

# @router.get("/articles/ai")
# async def articles_ai(
#     ids: List[int] = Query(...),
# ):
#     return await axioma_service.get_ai_articles_by_ids(token, ids)

# @router.get("/articles/{article_id}")
# async def article_by_id(article_id: int):
#     return await axioma_service.get_article_by_id(token, article_id)

# @router.get("/sources", response_model=list[SourceResponse])
# async def sources():
#     return await axioma_service.get_sources(token)

# @router.get("/sources/search", response_model=list[SourceResponse])
# async def search_sources(
#     name: Optional[str] = Query(None),
#     country: Optional[str] = Query(None),
# ):
#     return await axioma_service.search_sources(
#         token, name=name, country=country
#     )

# @router.get("/sources/countries")
# async def countries():
#     return await axioma_service.get_countries(token)

# @router.get("/sources/countries/search")
# async def search_country(name: str):
#     return await axioma_service.search_country(token, name)

# @router.post("/login")
# async def login(data: dict):
#     return await auth_service.login(data)

# @router.put("/profile")
# async def register(data: dict, token: str = Depends(require_token)):
#     return await auth_service.update(data, token)

# @router.get("/profile")
# async def profile(token: str = Depends(require_token)):
#     return await auth_service.get_profile(token)
