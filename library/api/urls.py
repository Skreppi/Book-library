from rest_framework.routers import DefaultRouter

from api.views import BooksViews

router = DefaultRouter()
router.register('books', BooksViews, basename='book')

urlpatterns = router.urls
