from django.test import TestCase
from .. import serializers

class Author(object):
    def __init__(self, name='', year=None, books=[]):
        self.name = name
        self.year = year
        self.books = books


class Book(object):
    def __init__(self, title=''):
        self.title = title


class Comic(Book):
    def __init__(self, color=True, **kwargs):
        super(Comic, self).__init__(**kwargs)
        self.color = color


class Novel(Book):
    def __init__(self, pages=None, **kwargs):
        super(Novel, self).__init__(**kwargs)
        self.pages = pages


class LibrarySerializer(serializers.DictSerializer):
    _classes = (
        ('Author', Author),
        ('Comic', Comic),
        ('Novel', Novel),
    )


class DictSerializerTest(TestCase):
    def test_author_default(self):
        # dump
        data = LibrarySerializer().dump(Author())
        self.assertEqual(data, dict(_class='Author', name='', year=None, books=[]))
        # load
        data = dict(_class='Author')
        author = LibrarySerializer().load(data)
        self.assertEqual(type(author), Author)
        self.assertEqual(author.name, '')
        self.assertEqual(author.year, None)
        self.assertEqual(author.books, [])

    def test_author_no_books(self):
        # dump
        author = Author(name='Isaac Asimov', year=1920)
        data = LibrarySerializer().dump(author)
        self.assertEqual(data, dict(_class='Author', name='Isaac Asimov', year=1920, books=[]))
        # load
        data = dict(_class='Author', name='Isaac Asimov', year=1920, books=[])
        author = LibrarySerializer().load(data)
        self.assertEqual(type(author), Author)
        self.assertEqual(author.name, 'Isaac Asimov')
        self.assertEqual(author.year, 1920)
        self.assertEqual(author.books, [])
        data = dict(_class='Author', name='Isaac Asimov', year=1920)
        author = LibrarySerializer().load(data)
        self.assertEqual(author.books, [])

    def test_books_dump(self):
        books = [
            Novel(title='The Naked Sun', pages=187),
            Comic(title='No way', color=False),
        ]
        author = Author(name='Isaac Asimov', year=1920, books=books)
        books = LibrarySerializer().dump(author)['books']
        self.assertEqual(type(books), list)
        self.assertEqual(len(books), 2)
        book = books[0]
        self.assertEqual(book, dict(_class='Novel', title='The Naked Sun', pages=187))
        book = books[1]
        self.assertEqual(book, dict(_class='Comic', title='No way', color=False))


    def test_books_load(self):
        data = dict(
            _class='Author',
            name='Isaac Asimov',
            year=1920,
            books=[
                dict(_class='Novel', title='The Naked Sun', pages=187),
                dict(_class='Comic', title='No way', color=False),
            ],
        )
        author = LibrarySerializer().load(data)
        book = author.books[0]
        self.assertEqual(type(book), Novel)
        self.assertEqual(book.title, 'The Naked Sun')
        self.assertEqual(book.pages, 187)
        book = author.books[1]
        self.assertEqual(type(book), Comic)
        self.assertEqual(book.title, 'No way')
        self.assertEqual(book.color, False)

    def test_book_list_dump(self):
        books = [
            Comic(title='Spiderman', color=True),
            Novel(title='The Naked Sun', pages=187),
        ]
        data = LibrarySerializer().dump(books)
        self.assertEqual(data[0], dict(_class='Comic', title='Spiderman', color=True))
        self.assertEqual(data[1], dict(_class='Novel', title='The Naked Sun', pages=187))

    def test_book_list_load(self):
        books = [
            dict(_class='Comic', title='Spiderman', color=True),
            dict(_class='Novel', title='The Naked Sun', pages=187),
        ]
        books = LibrarySerializer().load(books)
        self.assertEqual(type(books), list)
        self.assertEqual(type(books[0]), Comic)
        self.assertEqual(type(books[1]), Novel)

    def test_book_dict_dump(self):
        books = dict(
            spiderman=Comic(title='Spiderman', color=True),
            nakedsun=Novel(title='The Naked Sun', pages=187),
        )
        data = LibrarySerializer().dump(books)
        self.assertEqual(data['spiderman'], dict(_class='Comic', title='Spiderman', color=True))
        self.assertEqual(data['nakedsun'], dict(_class='Novel', title='The Naked Sun', pages=187))

    def test_book_dict_load(self):
        books = dict(
            spiderman=dict(_class='Comic', title='Spiderman', color=True),
            nakedsun=dict(_class='Novel', title='The Naked Sun', pages=187),
        )
        books = LibrarySerializer().load(books)
        self.assertEqual(type(books), dict)
        self.assertEqual(type(books['spiderman']), Comic)
        self.assertEqual(type(books['nakedsun']), Novel)
