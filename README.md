# API Introduction

## SFACGBook Class

### Initialize SFACGBook Instance

`SFACGBook(book_id: str)`

- `book_id`: The ID of the novel on SF Light Novel website, which must be in digital format.

### Methods

#### `get_book_info(self) -> dict`

Get basic information of the novel.

Return Value: A dictionary that contains the following fields:

- `book_name`: The name of the novel.
- `author_name`: The name of the author.
- `word_count`: The total number of words in the novel (in string format).
- `last_chapter_name`: The name of the latest chapter.
- `like_count`: The number of likes (in string format).
- `mark_count`: The number of bookmarks (in string format).
- `cover_url`: The URL of the cover image.
- `description`: The description of the novel.

#### `get_toc(self) -> dict`

Get the table of contents (list of chapters) of the novel.

Return Value: A dictionary that contains the following fields:

- `book_id`: The ID of the novel.
- `volume_list`: A list that contains the following fields:
    - `volume_index`: The index of the volume.
    - `chapter_index`: The index of the chapter.
    - `volume_name`: The name of the volume.
    - `chapter_name`: The name of the chapter.
    - `chapter_url`: The URL of the chapter.

#### `get_chapters(self, chapter_path: str) -> dict`

Get the content of a specific chapter.

Parameters:

- `chapter_path`: The URL of the chapter.

Return Value: A dictionary that contains the following fields:

- `book_id`: The ID of the novel.
- `volume_id`: The ID of the volume.
- `chapter_id`: The ID of the chapter.
- `chapter_path`: The URL of the chapter.
- `chapter_title`: The title of the chapter.
- `content`: The content of the chapter in string format. If it is a VIP chapter, it will return the string "VIP章节, 请使用app接口,web端无法获取正文信息".