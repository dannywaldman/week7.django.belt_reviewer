from django.shortcuts import render, redirect, HttpResponse
from .forms import UserForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Book, Review, Author
import bcrypt

def index(request):
    if 'user' in request.session:
        return redirect(reverse('books:books'))           
    return render(request, 'books/index.html', { 'form' : UserForm() })

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        errors = User.objects.validate(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error)
            return redirect(reverse('books:index'))
        else:
            user = form.save(commit=False)
            user.password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
            user.save()
            request.session['user'] = { 'id' : user.id }
            return redirect(reverse('books:books')) 
    
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('pw') 
        
    user = User.objects.filter(email = email).first()
        
    if user:
        valid_pw = bcrypt.checkpw(password.encode(), user.password.encode())
        if valid_pw:
            request.session['user'] = { 'id' : user.id }
            return redirect(reverse('books:books'))
        else:
            messages.error(request, 'Invalid user/password')
            return redirect(reverse('books:index'))                            
    else:
        messages.error(request, 'User does not exist')
        return redirect(reverse('books:index'))
    
def logout(request):
    name = User.objects.get(id=request.session.get('user')['id']).name
    request.session.clear()
    messages.success(request, '{} successfully logged out'.format(name))
    return redirect(reverse('books:index'))
    
def books(request):
    validate_login(request)
    context = {
        'books' : Book.objects.all(),
        'recent' : Review.objects.all().order_by('-created_at')[:3],
        'user' : User.objects.get(id=request.session.get('user')['id'])
    }
    print context
    return render(request, 'books/books.html', context)
    
def add(request):
    validate_login(request)
    return render(request, 'books/add.html', { 'authors' : Author.objects.all() })

def create(request):
    validate_login(request)
    if request.method == "POST":
        author_exist = request.POST.get('author')
        author_add = request.POST.get('author_add')
        if author_exist and author_add:
            messages.error(request, 'Only of the author fields can be used')
            return redirect(reverse('books:add'))          
        if not author_exist and not author_add:
            messages.error(request, 'At least of the author fields must be used')
            return redirect(reverse('books:add'))
        else:
            if author_add:
                author = Author.objects.create(name=author_add)
            else:
                author = Author.objects.get(id=int(author_exist))

            book = Book.objects.create(title=request.POST.get('title'), author=author)
            Review.objects.create(comment=request.POST.get('comment'), book=book, user=User.objects.get(id=request.session.get('user')['id']), rating=request.POST.get('rating'))
            return redirect(reverse('books:show_book', kwargs = {'id': book.id}))
    
def show_book(request, id):
    return render(request, 'books/show.html', { 'book' : Book.objects.get(id=id) })
    
def show_user(request, id):
    validate_login(request)
    user = User.objects.get(id=id)
    books = Review.objects.filter(user=user).values_list('book__id','book__title').distinct()
    return render(request, 'books/user.html', { 'user' : user, 'books' : books })
    
def add_review(request, id):
    validate_login(request)
    if request.method == "POST":
        Review.objects.create(comment = request.POST.get('comment'), rating = request.POST.get('rating'), book = Book.objects.get(id=id), user = User.objects.get(id=request.session.get('user')['id']))
        return redirect(reverse('books:show_book', kwargs={'id': id}))
    
def delete_review(request, id):
    validate_login(request)
    review = Review.objects.get(id=id)
    if review.user.id == request.session.get('user')['id']:
        review.delete()
    return redirect(reverse('books:show_book', kwargs={'id': review.book.id}))
             

def validate_login(request):
    if not 'user' in request.session:
        return redirect(reverse('books:index'))
   
