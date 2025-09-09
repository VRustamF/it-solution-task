from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy

from app_quotes.models import Quote

from random import choices

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



class NewQuoteView(CreateView):
    model = Quote
    template_name = 'app_quotes/new_quote.html'
    fields = ['text', 'source', 'weight']
    success_url = reverse_lazy('quotes:home')

    def form_valid(self, form):
        text = form.cleaned_data['text']
        source = form.cleaned_data['source']
        quotes = Quote.objects.all()

        if (quotes.filter(text=text, source=source)).exists():
            messages.error(self.request, message='Цитата уже существует!')
            return redirect('quotes:home')

        elif quotes.filter(source=source).count() >= 3:
                messages.error(self.request, message='Лимит цитат для этого источника достигнут!')
                return redirect('quotes:home')

        messages.success(self.request, 'Цитата успешно добавлена!')
        return super().form_valid(form)



class EditQuoteView(UpdateView):
    model = Quote
    fields = ['text', 'source', 'weight']
    template_name = 'app_quotes/edit_quote.html'
    success_url = reverse_lazy('quotes:home')

    def form_valid(self, form):
        text = form.cleaned_data['text']
        source = form.cleaned_data['source']
        quotes = Quote.objects.all()

        orig_quote = quotes.filter(id=self.object.id).first()

        source_changed = orig_quote.source != source

        if (quotes.filter(text=text, source=source)).exists():
            messages.error(self.request, message='Цитата уже существует!')
            return redirect('quotes:home')

        elif source_changed:
            if quotes.filter(source=source).count() >= 3:
                messages.error(self.request, message='Лимит цитат для этого источника достигнут!')
                return redirect('quotes:home')

        messages.success(self.request, 'Цитата успешно обновлена!')
        return super().form_valid(form)



class DashboardView(ListView):
    model = Quote
    template_name = 'app_quotes/dashboard.html'
    context_object_name = 'quotes'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Дашборд'
        context['current_order'] = self.request.GET.get('order', '-like')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        order = self.request.GET.get('order', '-like')
        if order in ['like', '-like', 'dislike', '-dislike', 'views', '-views', 'weight', '-weight']:
            queryset = queryset.order_by(order)
        return queryset



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

    context = {
        'random_quote': quote,
        'title': 'Случайная цитата',
               }

    return render(request, template_name='app_quotes/home.html', context=context)



def process_del_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.delete()
    messages.success(request, 'Цитата успешно удалена')
    return redirect('quotes:home')