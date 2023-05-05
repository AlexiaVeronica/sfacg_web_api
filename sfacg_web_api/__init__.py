import re
import requests
from lxml import etree
from retrying import retry


class SFACGBook:
    LOGIN_URL = "https://passport.sfacg.com/Ajax/QuickLogin.ashx"
    BOOK_URL = "https://book.sfacg.com/"

    def __init__(self):
        self.session = requests.Session()

    @retry(stop_max_attempt_number=3)
    def _get_html(self, url):
        response = self.session.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.82 Safari/537.36',
        })
        if response.status_code != 200:
            raise ValueError(f"get {url} error, status_code: {response.status_code}")
        return etree.HTML(response.text)

    @retry(stop_max_attempt_number=3)
    def _post_api(self, url, data):
        response = self.session.get(url, params=data, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        })
        return response

    def get_book_info(self, book_id):
        html = self._get_html(f"https://book.sfacg.com/Novel/{book_id}/")
        author = html.xpath('/html/body/div[1]/div[5]/div/div[1]/div[2]/div[2]/div[2]/p[1]/text()')[0]
        description = html.xpath('/html/body/div[1]/div[4]/div/div[1]/div[2]/p/text()')[0]
        cover_url = html.xpath('//*[@id="hasTicket"]/div[1]/div/div[1]/a/img/@src')
        book_name = html.xpath('/html/body/div[1]/div[4]/div/div[1]/div[2]/h3/span[1]/text()')
        word_count = html.xpath('/html/body/div[1]/div[6]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/p[1]/span/text()')
        last_chapter_name = html.xpath('/html/body/div[1]/div[4]/div/div[1]/div[2]/h3/a/text()')
        like_count = html.xpath('//*[@id="BasicOperation"]/a[2]/text()')
        mark_count = html.xpath('//*[@id="BasicOperation"]/a[3]/text()')
        return {
            'book_name': book_name[0].replace(">>", ""),
            'author_name': author,
            'word_count': word_count[0],
            "last_chapter_name": last_chapter_name[0],
            "like_count": like_count[0].replace("赞 ", ""),
            "mark_count": mark_count[0].replace("收藏 ", ""),
            'cover_url': cover_url[0],
            'description': description.strip(),
        }

    def get_toc(self, book_id):
        response = self._get_html(f"https://book.sfacg.com/Novel/{book_id}/MainIndex/")
        volume_list = {"book_id": book_id, "volume_list": []}
        volume_index = 0
        for volume in response.xpath('/html/body/div[1]/div[3]/div'):
            try:
                volume_name = volume.xpath(f'./div[1]/h3/text()')[0]
            except IndexError:
                continue
            volume_index += 1
            for index, chapter in enumerate(volume.xpath('./div[2]/ul/li'), start=1):
                chapter_name = chapter.xpath('./a/@title')[0]
                chapter_url = chapter.xpath('./a/@href')[0]
                volume_list["volume_list"].append(
                    {'volume_index': volume_index, 'chapter_index': index, 'volume_name': volume_name,
                     'chapter_name': chapter_name, 'chapter_url': chapter_url})
        return volume_list

    def get_chapters(self, book_id, chapter_path):
        if "vip" in chapter_path:
            return {
                "book_id": book_id,
                "chapter_path": chapter_path,
                "chapter_id": re.findall(r"/c/(\d+)/", chapter_path)[0],
                "content": "VIP章节, 请使用app接口,web端无法获取正文信息"
            }
        chapter_response = self._get_html(f"https://book.sfacg.com{chapter_path}")
        return {
            "book_id": book_id,
            "volume_id": chapter_path.split("/")[3],
            "chapter_id": chapter_path.split("/")[4],
            'chapter_path': chapter_path,
            'chapter_title': chapter_response.xpath('//*[@id="article"]/div[1]/h1/text()')[0],
            'content': '\n'.join(chapter_response.xpath('//*[@id="ChapterBody"]/p/text()'))
        }

    def login(self, name, password, al, session, sig, token, scene):
        if not name or not password:
            print("name or password is empty, please check your username and password")
            return
        if not al or not session or not sig or not token or not scene:
            print("al or session or sig or token or scene is empty, please check your al or session or sig or token or "
                  "scene")
            return

        url = "https://passport.sfacg.com/Ajax/QuickLogin.ashx"
        res = self._post_api(url, data={
            "name": name,
            "password": password,
            "al": al,
            "session": session,
            "sig": sig,
            "token": token,
            "scene": scene
        })
        if res.status_code == 200:
            return {
                "code": res.status_code,
                "message": "success",
                "SFCommunity": res.cookies[".SFCommunity"],
                "session_PC": res.cookies["session_PC"]
            }
        else:
            return {
                "code": res.status_code,
                "message": "login failed, please check your username and password",
            }
