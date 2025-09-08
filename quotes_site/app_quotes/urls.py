from django.urls import path

from app_quotes.views import HomeView, NewQuoteView, DashboardView, process_rate_quote, process_del_quote, EditQuoteView

app_name = 'quotes'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('new-quote/', NewQuoteView.as_view(), name='add_new_quote'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('vote/<int:quote_id>/like/', process_rate_quote, name='rate'),
    path('del-quote/<int:quote_id>/', process_del_quote, name='del_quote'),
    path('edit_quote/<int:pk>/', EditQuoteView.as_view(), name='edit_quote'),
]