import sfacg_web_api

from fastapi import FastAPI, HTTPException, Depends
from starlette.responses import HTMLResponse

app = FastAPI(
    title="SFACG WEB API",
)


async def get_sfacgbook():
    return sfacg_web_api.SFACGBook()


@app.middleware("http")
async def add_cors(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers[
        "Access-Control-Allow-Headers"] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    return response


@app.get("/login", response_class=HTMLResponse)
async def login_page():
    with open("login/login.html", "r", encoding="utf-8") as f:
        html = f.read()
    return html


@app.get("/api/login")
async def login(name: str, password: str, al: str, session: str, sig: str, token: str, scene: str,
                sfacg_book: sfacg_web_api.SFACGBook = Depends(get_sfacgbook)):
    if not name or not password:
        raise HTTPException(status_code=400, detail="username or password is empty")
    if not al or not session or not sig or not token or not scene:
        raise HTTPException(status_code=400, detail="al, session, sig, token, scene is empty")

    return sfacg_book.login(name, password, al, session, sig, token, scene)


@app.get("/api/book/{book_id}")
async def book_info(book_id: str, sfacg_book: sfacg_web_api.SFACGBook = Depends(get_sfacgbook)):
    if not book_id:
        raise HTTPException(status_code=400, detail="book_id is empty")
    book_info_json = sfacg_book.get_book_info(book_id)
    if book_info_json:
        return book_info_json
    else:
        raise HTTPException(status_code=400, detail="book_id is error")


@app.get("/api/book/{book_id}/chapter_list")
async def chapter_list(book_id: str, sfacg_book: sfacg_web_api.SFACGBook = Depends(get_sfacgbook)):
    if not book_id:
        raise HTTPException(status_code=400, detail="book_id is empty")
    chapter_list_json = sfacg_book.get_toc(book_id)
    if chapter_list_json:
        return chapter_list_json
    else:
        raise HTTPException(status_code=400, detail="book_id is error")


@app.get("/api/book/{book_id}/chapter/{chapter_id}")
async def chapter(book_id: str, chapter_id: str, sfacg_book: sfacg_web_api.SFACGBook = Depends(get_sfacgbook)):
    if not book_id or not chapter_id:
        raise HTTPException(status_code=400, detail="book_id or chapter_id is empty")
    chapter_json = sfacg_book.get_chapters(book_id, chapter_id)
    if chapter_json:
        return chapter_json
    else:
        raise HTTPException(status_code=400, detail="book_id or chapter_id is error")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", reload=True)
