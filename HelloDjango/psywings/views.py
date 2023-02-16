from .models import Dictionary, ALPHABET_CHOICES
from .models import Post
from .models import Links
from .models import CategoryPost
from .models import EventCategory
from .models import Event
from .models import Books
from .models import Gallery
from .models import CategoryGallery
from .models import Choice, Question
from django.views.generic import ListView
from django.views.generic import DetailView
from itertools import chain
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
import calendar
from calendar import HTMLCalendar
from datetime import datetime


class DictList(ListView):
    model = Dictionary
    template_name = 'psywings/dictionary_list.html'
    context_object_name = 'dictionary'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):

        list_items = Dictionary.objects.alphabetized_list()
        context = {
          'object_list': list_items,
          'alphabet': ALPHABET_CHOICES,
        }
        return context

    def get_queryset(self):
        return Dictionary.objects.alphabetized_list()


class SearchView(ListView):
    template_name = 'psywings/search.html'
    paginate_by = 10
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = f"q={self.request.GET.get('q')}&"
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            post_results = Post.objects.search(query)
            dict_results = Dictionary.objects.search(query)
            book_result = Books.objects.search(query)

            # combine querysets
            queryset_chain = chain(post_results, dict_results,book_result)
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)

            self.count = len(qs)  # since qs is actually a list
            return qs
        return Post.objects.none()  # just an empty queryset as default


class ViewLinks(ListView):
    template_name = 'psywings/links.html'
    context_object_name = 'links'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Links.objects.all()


class PollsView(generic.ListView):
    template_name = 'psywings/polls.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailPollView(generic.DetailView):
    model = Question
    template_name = 'psywings/detail_poll.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'psywings/poll_results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'psywings/detail_poll.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('psywings:results_poll', args=(question.id,)))


class ViewByPostCategory(ListView):
    model = Post
    template_name = 'psywings/post_category.html'
    context_object_name = 'post_category'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = CategoryPost.objects.get(pk=self.kwargs['post_category_id'])
        return context

    def get_queryset(self):
        return CategoryPost.objects.filter(post_category_id=self.kwargs['post_category_id'], is_published=True)


class ViewPosts(ListView):
    Model = Post
    template_name = 'psywings/posts.html'
    context_object_name = 'posts'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Post.objects.all()


class ShowPost(DetailView):
    model = Post
    allow_empty = True
    template_name = 'psywings/view_post.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ViewEvents(ListView):
    Model = Event
    template_name = 'psywings/all_events.html'
    context_object_name = 'events'
    paginate_by = 10
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Event.objects.all()


class ShowEvent(DetailView):
    model = Event
    allow_empty = True
    template_name = 'psywings/view_event.html'
    context_object_name = 'event'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ViewByEventCatedory(ListView):
    model = Event
    template_name = 'psywings/events_category.html'
    context_object_name = 'category_events'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = EventCategory.objects.get(pk=self.kwargs['event_category_id'])
        return context

    def get_queryset(self):
        return Event.objects.filter(event_category_id=self.kwargs['event_category_id'], is_published=True)


class ViewBooks(ListView):
    template_name = 'psywings/books.html'
    context_object_name = 'books'
    allow_empty = True
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Books.objects.all()


class ViewGallery(ListView):
    template_name = 'psywings/all_images.html'
    context_object_name = 'gallery'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Gallery.objects.all()


class ShowImageGallery(DetailView):
    model = Gallery
    allow_empty = True
    template_name = 'psywings/one_image.html'
    context_object_name = 'image_gallery'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ViewByGalleryCategory(ListView):
    model = Gallery
    template_name = 'psywings/category_images.html'
    context_object_name = 'category_images'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = CategoryGallery.objects.get(pk=self.kwargs['image_category_id'])
        return context

    def get_queryset(self):
        return Gallery.objects.filter(image_category_id=self.kwargs['image_category_id'], is_published=True)


def view_calendar(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    event_calendar = HTMLCalendar().formatmonth(year, month_number)
    now = datetime.now()
    current_year = now.year

    event_list = Event.objects.filter(
        event_date__year = year,
        event_date__month = month_number
    )

    return render(request, 'psywings/calendar.html',
                  {'year': year,
                   'month': month,
                   'month_number': month_number,
                   'event_calendar': event_calendar,
                   'current_year': current_year,
                   'event_list': event_list,}
                   )
