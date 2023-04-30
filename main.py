import sfacg_web_api

if __name__ == '__main__':

    sf = sfacg_web_api.SFACGBook("629008")
    book_info = sf.get_book_info()
    print(book_info)
    chapter_list = sf.get_toc()
    print(chapter_list)
    for chapter in chapter_list["volume_list"]:
        print(chapter["volume_name"] + " : " + chapter["chapter_name"])
        print(sf.get_chapters(chapter["chapter_url"]))
