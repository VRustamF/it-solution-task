from lib2to3.fixes.fix_input import context
from random import choices
from shlex import quote

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.db.models import Count, Sum
from django.contrib import messages

from app_quotes.models import Quote

# Create your views here.



class HomeView(ListView):
    model = Quote
    template_name = 'app_quotes/home.html'
    context_object_name = 'quotes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Случайная цитата'

        if context['quotes']:
            quote = choices(context['quotes'], weights=[el.weight for el in context['quotes']])[0]
            quote.views += 1
            quote.save()
            context['random_quote'] = quote
        return context



class NewQuoteView(View):
    template_name = 'app_quotes/new_quote.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        text = request.POST.get('text')
        source = request.POST.get('source')
        weight = request.POST.get('weight') or 1

        quotes = Quote.objects.all()

        if (not quotes.filter(text=text, source=source).exists() and
                quotes.filter(source=source).aggregate(Count('source'))['source__count'] < 3):
            new_quote = Quote(text=text, source=source, weight=weight)
            new_quote.save()
            messages.success(request, 'Цитата успешно добавлена!')
        else:
            messages.error(request, 'Цитата уже существует или лимит для источника достигнут.')

        return redirect('quotes:home')



class DashboardView(ListView):
    model = Quote
    template_name = 'app_quotes/dashboard.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Дашборд хз'
        return context



def process_rate_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    action = request.POST.get('action_type')
    session_key = f'voted_{quote_id}'

    if not request.session.get(session_key):
        if action == 'like':
            quote.like += 1
            quote.save()
            request.session[session_key] = 'like'
            messages.success(request, 'Вы поставили лайк!')
        else:
            quote.dislike += 1
            quote.save()
            request.session[session_key] = 'dislike'
            messages.success(request, 'Вы поставили дизлайк!')
    else:
        msg = 'Вы уже лайкали эту цитату!' if request.session.get(
            session_key) == 'like' else 'Вы уже дизлайкали эту цитату!'
        messages.info(request, message=msg)

    context = {'random_quote': quote}

    return render(request, template_name='app_quotes/home.html', context=context)



def process_del_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.delete()
    messages.success(request, 'Цитата успешно удалена')
    return redirect('quotes:home')



def process_edit_quote(request, quote_id):
    pass