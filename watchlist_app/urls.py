from django.urls import path,include
from watchlist_app.views import WatchDetail,WatchListFN,StreamPlatformFN,StreamDetail,ReviewListFN,ReviewDetailFN

urlpatterns = [
    path('list/',WatchListFN),
    path('list/<int:id>/',WatchDetail),
    path('stream/',StreamPlatformFN),
    path('<int:id>',StreamDetail),
    path('<int:id>/reviews',ReviewListFN),
    path('review/<int:id>',ReviewDetailFN)
]