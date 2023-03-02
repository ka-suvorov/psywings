from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticSitemap, PostDetailSitemap, GalleryDetailSitemap, FriendDetailSitemap, PersonaDetailSitemap


app_name = 'pages'
urlpatterns = [
    path("", view_landing, name ="index"),
    path("post/", ViewPosts.as_view(), name="posts"),
    path('dictionary/', DictList.as_view(), name='dictionary_list'),
    path('search/', SearchView.as_view(), name='search'),
    path('links/', ViewLinks.as_view(), name='links'),
    path('friends/', ViewLFriends.as_view(), name='friends'),
    path('friends/<int:pk>/', ViewFriendLinkDetail.as_view(), name='friend'),
    path('persons/', ViewPersons.as_view(), name='persons'),
    path('persona/<int:pk>/', ShowPersona.as_view(), name='persona'),
    path('polls/', PollsView.as_view(), name='polls'),
    path('detail_poll/<int:pk>/', DetailPollView.as_view(), name='detail_poll'),
    path('poll/<int:pk>/results/', ResultsView.as_view(), name='results_poll'),
    path('vote/<int:question_id>/vote/', vote, name='vote'),
    # path('category/<int:post_category_id>/', ViewByPostCategory.as_view(), name='get_post_category'),
    path('category/<int:category_id>/', get_category, name='get_post_category'),
    path('post/<int:pk>/', ShowPost.as_view(), name='view_post'),
    path('events/', ViewEvents.as_view(), name='events'),
    path('events/category/<int:event_category_id>/', ViewByEventCatedory.as_view(), name='events_category'),
    path('event/<int:pk>/', ShowEvent.as_view(), name='view_event'),
    path('books/', ViewBooks.as_view(), name='books'),
    path('gallery/', ViewGallery.as_view(), name='psy_gallery'),
    path('gallery_category/<int:image_category_id>/', ViewByGalleryCategory.as_view(), name='get_gallery_category'),
    path('gallery/<int:pk>/', ShowImageGallery.as_view(), name='image_gallery'),
    path('calendar/', view_calendar, name='month_event_calendar'),
    path('suvorov/', view_suvorov, name='suvorov'),

       ]

urlpatterns += staticfiles_urlpatterns()

sitemaps = {
    'pages': StaticSitemap,
    'post': PostDetailSitemap,
    'image_gallery': GalleryDetailSitemap,
    'friend': FriendDetailSitemap,
    'persona': PersonaDetailSitemap,
 }

urlpatterns += [
    re_path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

]