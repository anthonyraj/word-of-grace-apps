import requests
import re
from pathlib import Path
from yattag import Doc

"""
    BlogPost class helps fetch the blog posts from wordpress using wp-json REST api
    https://developer.wordpress.org/rest-api/reference/posts
"""

class BlogPost:
    def __init__(self,page_count=10):
        self.url = "http://www.wordofgracechurch.org/wp-json/wp/v2/posts"
        self.posts = []
        self.page_count = page_count
        self.url_regex = r'https://[\w\.]+[/\w%20]+.mp3'
        self.html_folder = Path('html')
        self.html_extension = 'html'

    def fetch_posts(self):
        for page in range(1,self.page_count):
            feed_url = "{}?page={}".format(self.url,str(page))
            response = requests.get(feed_url)
            self.filter_posts(response.json())

    def filter_posts(self,json_data):
        for item in json_data:
            if isinstance(item,dict):
                post = self.parse_attributes(item)
                if 'audio_url' in post.keys():
                    self.posts.append(post)
                else: print('missing audio url')
            else:
                print("something went wrong!")

    def parse_attributes(self,item):
        item_keys = item.keys()
        title,blog_url,audio_url = "N/A","N/A","N/A"
        post = {}
        if 'title' in item_keys:
            post['title'] = item['title']['rendered']
        if 'link' in item_keys:
            post['blog_url'] = item['link']
        if 'content' in item_keys:
            audio_url = self.find_audio_url(item['content']['rendered'])
            if audio_url: post['audio_url'] = audio_url
        return post

    def find_audio_url(self,content):
        url = re.findall(self.url_regex,content)
        if len(url): return url[0]
        else: return ""

    def list_posts(self):
        for item in self.posts:
            print(item)

    def total_posts(self):
        print("Total posts with audio recording: {}".format(len(self.posts)))
        return len(self.posts)

    def create_output_file(self,title):
        html_file = '{}.{}'.format('-'.join(title.lower().split()), self.html_extension)
        return self.html_folder / html_file

    def write_posts(self,title="Word of Grace Posts"):
        output_html = self.create_output_file(title)
        with open(output_html,'w+') as file:
            generated_html = self.generate_html(title)
            file.write(generated_html)

    def generate_html(self,title):
        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('title'):
                text(title)
            with tag('body'):
                with tag('h3'):
                    text(title)
                with tag('ol', id='sermon list'):
                    for index,post in enumerate(self.posts):
                        with tag('li', number=index, id='sermon post'):
                            with tag('p'):
                                with tag('a', href=post['blog_url']):
                                    text('[Blog]')
                                # doc.asis(' | ')
                                # with tag('a', href=post['audio_url']+'?dl=1'):
                                #      text('[Download Audio]')
                                text(' Title: {}'.format(post['title']))
                                doc.asis('<audio controls src={} type="audio/mpeg"/>'.format(post['audio_url']))
                        doc.stag('hr')

        return doc.getvalue()

blog = BlogPost(10)
blog.fetch_posts()
#blog.list_posts()
blog.write_posts(title='Word of Grace Posts 8 Sept 2018')
blog.total_posts()
