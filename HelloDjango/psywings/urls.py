from django.urls import path, re_path
from .views import *
from django.conf.urls import url


app_name = 'psywings'
urlpatterns = [
    path("post/", ViewPosts.as_view(), name ="posts"),
    path('dictionary/', DictList.as_view(), name='dictionary_list'),
    path('search/', SearchView.as_view(), name='search_all'),
    path('links/', ViewLinks.as_view(), name='links'),
    path('polls/', PollsView.as_view(), name='polls'),
    path('<int:pk>/', DetailPollView.as_view(), name='detail_poll'),
    path('<int:pk>/results/', ResultsView.as_view(), name='results_poll'),
    path('<int:question_id>/vote/', vote, name='vote'),
    path('category/<int:post_category_id>/', ViewByPostCategory.as_view(), name='get_post_category'),
    path('post/<int:pk>/', ShowPost.as_view(), name='view_post'),
    path('events/', ViewEvents.as_view(), name='events'),
    path('events/category/<int:event_category_id>/', ViewByEventCatedory.as_view(), name='events_category'),
    path('event/<int:pk>/', ShowEvent.as_view(), name='view_event'),
    path('books/', ViewBooks.as_view(), name='books'),
    path('gallery/', ViewGallery.as_view(), name='psy_gallery'),
    path('gallery_category/<int:image_category_id>/', ViewByGalleryCategory.as_view(), name='get_gallery_category'),
    path('gallery/<int:pk>/', ShowImageGallery.as_view(), name='image_gallery'),
    path('calendar/', view_calendar, name='month_event_calendar'),
    ]