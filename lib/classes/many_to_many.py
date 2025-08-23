class Article:

    all = []

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # only allow setting once
        if hasattr(self, "_title"):
            return

        if not isinstance(value, str):
            return

        if not (5 <= len(value) <= 50):
            return

        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        from classes.many_to_many import Author
        if not isinstance(value, Author):
            return
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        from classes.many_to_many import Magazine
        if not isinstance(value, Magazine):
            return
        self._magazine = value


class Author:

    all = []

    def __init__(self, name):
        self.name = name
        Author.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):

        if hasattr(self, "_name"):
            return

        if not isinstance(value, str):
            return

        if len(value) == 0:
            return

        self._name = value

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        #     mags = self.magazines()
        #    if not mags:
        #          return None
        areas = list({magazine.category for magazine in self.magazines()})
        if not areas:
            return None

        return areas


class Magazine:
    all = []

    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters.")

        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")

        if len(value) == 0:
            raise TypeError("Categories must be longer than 0 characters.")
        self._category = value

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list(set([article.author for article in Article.all if article.magazine == self]))

    def article_titles(self):
        titles = [
            article.title for article in Article.all if article.magazine == self]

        return titles if titles else None


    def contributing_authors(self):
        authors_count = {}

        for article in self.articles():
            author = article.author
            authors_count[author] = authors_count.get(author, 0) + 1

        result = [author for author, count in authors_count.items() if count > 2]

        return result if result else None
