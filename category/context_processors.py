
from .models import Category

def menu_links(request):

    #links will fetch all the categories from database here
    links = Category.objects.all()
    # dict function will cover all links in dictionary format
    return dict(links=links) 
