    
from category.models import Category

# custom context processor to show categories in navbar
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)    
    
