from library.models import Category

def navbar_content(request):
    categories = Category.objects.all()
    return {'categories': categories}
