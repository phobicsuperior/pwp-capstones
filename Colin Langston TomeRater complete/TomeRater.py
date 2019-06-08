from random import randint
library = []


class User:
	def __init__(self, name, email):
		self.name = name
		self.email = email
		self.books = {}

	def __repr__(self):
		return "User {name}, email: {email}, books read: {books}".format(name=self.name, email=self.email, books=len(self.books))

	def __eq__(self, other_user):
		return self.name == other_user.name and self.email == other_user.email

	def get_email(self):
		return self.email
	
	def get_average_rating(self):
		current_avg = 0

		for ea in self.books:
			if self.books[ea] is None:
				pass
			else:
				current_avg += self.books[ea]
		if len(self.books) > 0:
			current_avg = current_avg / len(self.books)
			return current_avg
		return "{name} hasn't read any books yet.".format(name=self.name)
		
	def change_email(self, address):
		self.email = address
		print("User {name}'s email address has been updated to: {new}".format(name=self.name, new=address))

	def read_book(self, book, rating=None):
		self.books[book] = rating


class Book:
	def __init__(self, title, isbn):
		self.title = title
		self.isbn = isbn
		self.ratings = []
		self.unique_id = ""
		while len(self.unique_id) < 10:
			self.unique_id += str(randint(0, 9))
		if self.unique_id in library:
			self.unique_id += "a"
		library.append(self.unique_id)

	def __repr__(self):
		return self.title

	def __eq__(self, other_book):
		return self.title == other_book.title and self.isbn == other_book.isbn
		
	def get_title(self):
		return self.title
		
	def get_isbn(self):
		return self.isbn
	
	def set_isbn(self, new_isbn):
		self.isbn = new_isbn
		print("{title}'s ISBN has been updated to: {new}".format(title=self.title, new=self.isbn))
	
	def add_rating(self, rating):
		if rating is None:
			pass
		elif rating < 0 or rating > 4:
			print("Invalid rating.")
		else:
			self.ratings.append(rating)
			
	def get_average_rating(self):
		current_avg = 0
		for ea in self.ratings:
			current_avg += ea
		if len(self.ratings) > 0:
			return current_avg / len(self.ratings)
		return "This book is not yet rated."
		
	def __hash__(self):
		return hash(self.unique_id)


class Fiction(Book):
	def __init__(self, title, author, isbn):
		super().__init__(title, isbn)
		self.author = author
		
	def __repr__(self):
		return "{title} by {author}".format(title=self.title, author=self.author)


class NonFiction(Book):
	def __init__(self, title, subject, level, isbn):
		super().__init__(title, isbn)
		self.subject = subject
		self.level = level
		
	def get_subject(self):
		return self.subject
		
	def get_level(self):
		return self.level.title()
		
	def __repr__(self):
		var = "a"
		if self.level[0].lower() in "aeiou":
			var = "an"
		return "{title}, {var} {level} manual on {subject}".format(title=self.title, var=var, level=self.level, subject=self.subject)


class TomeRater:
	def __init__(self):
		self.users = {}
		self.books = {}

	def create_book(self, title, isbn):
		if self.title_check(title):
			book = Book(title, isbn)
			self.books[book] = 0
			return book
		print("This book has already been created!")
		return None

	def create_novel(self, title, author, isbn):
		if self.title_check(title):
			book = Fiction(title, author, isbn)
			self.books[book] = 0
			return book
		print("This book has already been created!")
		return None
		
	def create_non_fiction(self, title, subject, level, isbn):
		if self.title_check(title):
			book = NonFiction(title, subject, level, isbn)
			self.books[book] = 0
			return book
		print("This book has already been created!")
		return None

	def title_check(self, title):
		check = True
		for ea in self.books:
			if ea.title == title:
				check = False
		return check

	def add_book_to_user(self, book, email, rating=None):
		if email not in self.users:
			print("No user with email {email}!".format(email=email))
		else:
			if book not in self.books:
				self.books[book] = 0
			self.users[email].read_book(book, rating)
			book.add_rating(rating)
			self.books[book] += 1
				
	def add_user(self, name, email, user_books=None):
		self.users[email] = User(name, email)
		if user_books is not None:
			for book in user_books:
				self.add_book_to_user(book, email)
				
	def print_catalog(self):
		for book in self.books.keys():
			print(book)
			
	def print_users(self):
		for user in self.users.values():
			print(user)
			
	def most_read_book(self):
		current = 0
		title = ""
		for ea in self.books:
			if self.books[ea] > current:
				current = self.books[ea]
				title = ea.title
		return "{book} is the most-read book. It has been read {number} times!".format(book=title, number=current)
	
	def highest_rated_book(self):
		current = 0
		title = ""
		for ea in self.books.keys():
			if ea.get_average_rating() > current:
				current = ea.get_average_rating()
				title = ea.title
		return "{book} is the highest-rated book, with an average rating of {rating}!".format(book=title, rating=current)
		
	def most_positive_user(self):
		current = 0
		name = ""
		for ea in self.users:
			avg = self.users[ea].get_average_rating()
			if avg > current:
				current = self.users[ea].get_average_rating()
				name = ea
		return "The most positive user is {name}- Their average book rating is {rating}!".format(name=name, rating=current)

	def most_recently_added(self):
		for ea in self.books:
			if ea.unique_id == library[-1]:
				return "The most recently added book is {title}!".format(title=ea)


"""
KNOWN BUGS:

None at this time.

CURRENT IMPROVEMENT PROJECTS:

None at this time.

COMPLETED IMPROVEMENT PROJECTS:

1. Added code in non-fiction to change whether "a" or "an" is printed based on the first letter of the level
2. ***OBSOLETE*** Added code in Book's __eq__ and .set_isbn() methods to keep track of past ISBNs- if a book's ISBN was
changed after it was added to TomeRater.books, TomeRater either thought it was a new book or threw a KeyError
3. Changed book creation to add the books it creates to TomeRater.books with a read count of 0
4. Accordingly, changed add_book_to_user() to account for books to already be in TomeRater.books with a count of 0
5. Made sure that add_book_to_user() can still accept books not in TomeRater.books (Just in case someone decides to add
a book by saying example = Book("Title", 12345))
6. Updated Book's identification- Since ISBN is mutable with the set_isbn() method, it is unreliable as an identifier.
Added a .unique_id string in .__init__() which generates a random 10 digit identifier for every book. Also updated the
hash and eq methods to key off the unique identifier rather than the title and ISBN.
7. Added a library- a list of all unique IDs used so far. Also added what to do in the (extremely unlikely) event that
two books generate identical unique IDs. Might get unwieldy after a few million books, but until then it will work just
fine.
8. Added a method in TomeRater to check if a book had already been created- keys off title, so not as good as using
unique_id, but certainly better than ISBN.
9. Since creating new books now has an impact on things outside of the book object itself, moved where the book creation
actually happens in the .create_* methods in TomeRater to avoid filling up the library with extraneous unique IDs.
10. Added a method to TomeRater to show which book was most recently added to the library.
"""
