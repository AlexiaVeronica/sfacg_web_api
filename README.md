# SFACGBook Class README

This is a Python class that provides an interface to retrieve book information, table of contents, and chapter content
from the website sfacg.com.

## Prerequisites

- Python 3.6 or later
- [Requests](https://pypi.org/project/requests/) library
- [lxml](https://pypi.org/project/lxml/) library
- [retrying](https://pypi.org/project/retrying/) library

## Usage

To use this class, you can create an instance of `SFACGBook` by importing the module and calling its constructor.

```python
from sfacg import SFACGBook

book = SFACGBook()
```

### Login

You can log in to your account with the `login` method, which takes the following parameters:

```python
def login(self, name, password, al, session, sig, token, scene):
```

- `name`: Your username.
- `password`: Your password.
- `al`: The "al" parameter obtained from the login page response.
- `session`: The "session" parameter obtained from the login page response.
- `sig`: The "sig" parameter obtained from the login page response.
- `token`: The "token" parameter obtained from the login page response.
- `scene`: The "scene" parameter obtained from the login page response.

The method returns a dictionary containing the status code, message, and cookies.

### Get Book Information

You can get the information of a book with the `get_book_info` method, which takes the book ID as a parameter:

```python
def get_book_info(self, book_id):
```

The method returns a dictionary containing the book's name, author's name, word count, last chapter name, like count,
mark count, cover URL, and description.

### Get Table of Contents

You can get the table of contents of a book with the `get_toc` method, which takes the book ID as a parameter:

```python
def get_toc(self, book_id):
```

The method returns a dictionary containing the book's ID and a list of volumes (each with its own index, name, and a
list of chapters, each with its own index, name, and URL).

### Get Chapter Content

You can get the content of a chapter with the `get_chapters` method, which takes the book ID and chapter path as
parameters:

```python
def get_chapters(self, book_id, chapter_path):
```

The method returns a dictionary containing the book's ID, volume ID, chapter ID, chapter path, chapter title, and
chapter content.

