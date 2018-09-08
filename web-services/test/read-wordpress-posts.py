import requests
import re

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

    def write_posts(self,output_html):
        with open(output_html,'w+') as file:
            file.write('<h3>Word of Grace Posts</h3>')
            file.write('<ul>')
            for item in self.posts:
                file.write('<li><p>{}</p>'.format(item['title']))
                file.write('<p>{}</p>'.format(item['blog_url']))
                file.write('<p><a href="{}">{}</a></p></li>'.format(item['audio_url'],item['audio_url']))
            file.write('</ul>')

blog = BlogPost(10)
blog.fetch_posts()
#blog.list_posts()
blog.write_posts('html/word-of-grace-posts.html')
blog.total_posts()
