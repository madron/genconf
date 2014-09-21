import netaddr
from django.test import TestCase
from .. import serializers

class Author(object):
    def __init__(self, name='', year=None, books=[]):
        self.name = name
        self.year = year
        self.books = books


class Edition(object):
    def __init__(self, year=None):
        self.year = year


class Book(object):
    def __init__(self, title='', edition=None):
        self.title = title
        self.edition = edition


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
        ('Edition', Edition),
        ('Comic', Comic),
        ('Novel', Novel),
    )


class Netaddr(object):
    def __init__(
        self,
        ipaddress=netaddr.IPAddress('192.168.1.1'),
        ipnetwork=netaddr.IPNetwork('192.168.1.5/24')
    ):
        self.ipaddress = netaddr.IPAddress(ipaddress)
        self.ipnetwork = netaddr.IPNetwork(ipnetwork)


class NetaddrSerializer(serializers.DictSerializer):
    _classes = (
        ('netaddr', Netaddr),
        ('ipaddress', netaddr.IPAddress),
        ('ipnetwork', netaddr.IPNetwork),
    )

    def dump_ipaddress(self, obj):
        return str(obj)

    def dump_ipnetwork(self, obj):
        return str(obj)


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
            Novel(title='The Naked Sun', pages=187, edition=Edition(year=1957)),
            Comic(title='No way', color=False),
        ]
        author = Author(name='Isaac Asimov', year=1920, books=books)
        books = LibrarySerializer().dump(author)['books']
        self.assertEqual(type(books), list)
        self.assertEqual(len(books), 2)
        book = books[0]
        self.assertEqual(len(book), 4)
        self.assertEqual(book['_class'], 'Novel')
        self.assertEqual(book['title'], 'The Naked Sun')
        self.assertEqual(book['pages'], 187)
        self.assertEqual(book['edition'], dict(_class='Edition', year=1957))
        book = books[1]
        self.assertEqual(len(book), 4)
        self.assertEqual(book['_class'], 'Comic')
        self.assertEqual(book['title'], 'No way')
        self.assertEqual(book['color'], False)
        self.assertEqual(book['edition'], None)


    def test_books_load(self):
        data = dict(
            _class='Author',
            name='Isaac Asimov',
            year=1920,
            books=[
                dict(_class='Novel', title='The Naked Sun', pages=187, edition=dict(_class='Edition', year=1957)),
                dict(_class='Comic', title='No way', color=False),
            ],
        )
        author = LibrarySerializer().load(data)
        book = author.books[0]
        self.assertEqual(type(book), Novel)
        self.assertEqual(book.title, 'The Naked Sun')
        self.assertEqual(book.pages, 187)
        self.assertEqual(type(book.edition), Edition)
        self.assertEqual(book.edition.year, 1957)
        book = author.books[1]
        self.assertEqual(type(book), Comic)
        self.assertEqual(book.title, 'No way')
        self.assertEqual(book.color, False)
        self.assertEqual(book.edition, None)

    def test_book_list_dump(self):
        books = [
            Comic(title='Spiderman', color=True),
            Novel(title='The Naked Sun', pages=187),
        ]
        data = LibrarySerializer().dump(books)
        self.assertEqual(data[0], dict(_class='Comic', title='Spiderman', color=True, edition=None))
        self.assertEqual(data[1], dict(_class='Novel', title='The Naked Sun', pages=187, edition=None))

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
        self.assertEqual(data['spiderman'], dict(_class='Comic', title='Spiderman', color=True, edition=None))
        self.assertEqual(data['nakedsun'], dict(_class='Novel', title='The Naked Sun', pages=187, edition=None))

    def test_book_dict_load(self):
        books = dict(
            spiderman=dict(_class='Comic', title='Spiderman', color=True),
            nakedsun=dict(_class='Novel', title='The Naked Sun', pages=187),
        )
        books = LibrarySerializer().load(books)
        self.assertEqual(type(books), dict)
        self.assertEqual(type(books['spiderman']), Comic)
        self.assertEqual(type(books['nakedsun']), Novel)

    def test_netaddr_dump(self):
        net = Netaddr(
            ipaddress='192.168.100.100',
            ipnetwork='10.10.10.10/16',
        )
        self.assertEqual(type(net), Netaddr)
        self.assertEqual(type(net.ipaddress), netaddr.IPAddress)
        self.assertEqual(type(net.ipnetwork), netaddr.IPNetwork)
        net = NetaddrSerializer().dump(net)
        self.assertEqual(
            net,
            dict(
                _class='netaddr',
                ipaddress='192.168.100.100',
                ipnetwork='10.10.10.10/16',
            )
        )

    def test_netaddr_load(self):
        net = dict(_class='netaddr',
            ipaddress='192.168.100.100',
            ipnetwork='10.10.10.10/16',
        )
        net = NetaddrSerializer().load(net)
        self.assertEqual(type(net), Netaddr)
        self.assertEqual(type(net.ipaddress), netaddr.IPAddress)
        self.assertEqual(type(net.ipnetwork), netaddr.IPNetwork)
        self.assertEqual(net.ipaddress, netaddr.IPAddress('192.168.100.100'))
        self.assertEqual(net.ipnetwork, netaddr.IPNetwork('10.10.10.10/16'))
