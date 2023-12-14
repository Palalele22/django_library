from library.models import Book

class Cart():
    def __init__(self, request):
        self.session = request.session
        
        cart = self.session.get('session_key')
        
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        self.cart = cart
    
    def add(self, book):
        book_id = str(book.id)
        
        # logic
        if book_id in self.cart:
            pass
        else:
            self.cart[book_id] = {'author': book.author}
            
        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)
    
    def get_books(self):
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)
        
        return books
    
    
    def delete(self, book):
        book_id = str(book)
        if book_id in self.cart:
            del self.cart[book_id]
        
        self.session.modified = True    
    