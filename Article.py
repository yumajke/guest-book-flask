class Article:
    id = 0

    def __init__(self, title, content):
        Article.id += 1
        self.id = Article.id
        self.title = title
        self.content = content
        self.comments = []

    def get_title(self):
        return self.title

    def get_content(self):
        return self.content

    def get_comments(self):
        return self.comments

    def add_comment(self, title, content):
        self.comments.append(Article(title, content))

    def get_id(self):
        return self.id
