from django.urls import path

from .views import AddItemView, GetItemView, PostReviewView

urlpatterns = [
    path('api/v1/goods/', AddItemView.as_view()),
    path('api/v1/goods/<int:item_id>/', GetItemView.as_view()),
    path('api/v1/goods/<int:item_id>/reviews/', PostReviewView.as_view()),
]

# curl -v -d '{"title": "Сыр \"Российский\"","description": "Очень вкусный сыр, да еще и российский.","price": 100}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/v1/goods/
# curl -v -d '{"text": "Best. Cheese. Ever.","grade": 9}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/v1/goods/1/reviews/

# curl -v -H "Content-Type: application/json" -X GET http://localhost:8000/api/v1/goods/:id/


