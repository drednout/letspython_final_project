from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import redis
from final.settings import PLAYERS_PAGINATE_BY
from forms import PlayerSearchForm, MyAuthenticationForm, ChangeExpForm
from models import Players


class PlayersListView(FormMixin, ListView):
    model = Players
    context_object_name = 'playerslist'
    template_name = 'admintool/players.html'
    paginate_by = PLAYERS_PAGINATE_BY
    form_class = PlayerSearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Players.objects.filter(email__regex=form.cleaned_data['email'])
        return Players.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PlayersListView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlayersListView, self).dispatch(*args, **kwargs)


class PlayerDetailView(DetailView):
    model = Players
    context_object_name = 'player'
    template_name = 'admintool/player.html'
    pk_url_kwarg = 'player_id'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlayerDetailView, self).dispatch(*args, **kwargs)


class ExpUpdateView(UpdateView):
    model = Players
    template_name = 'admintool/changeexp.html'
    pk_url_kwarg = 'player_id'
    initial = {'xp': ''}
    form_class = ChangeExpForm
    success_url = '/players/'
    context_object_name = 'player'

    @method_decorator(login_required)
    @method_decorator(permission_required('admintool.change_exp', login_url='/access_denied/'))
    def dispatch(self, *args, **kwargs):
        return super(ExpUpdateView, self).dispatch(*args, **kwargs)


class LoginFormView(FormView):
    form_class = MyAuthenticationForm
    template_name = "admintool/login.html"

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return '/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


def logout_user(request):
    logout(request)
    return redirect('/')


def mainpage(request):
    return render(request, 'admintool/mainpage.html')


def access_denied(request):
    return render(request, 'admintool/access_denied.html')


def show_redis_data(request):
    redis_con = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_data = redis_con.zrevrange(name='scores', start=0, end=-1, withscores=True)
    paginator = Paginator(redis_data, PLAYERS_PAGINATE_BY)
    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data = paginator.page(paginator.num_pages)
    template_data = {
        'data': data
    }
    return render(request, 'admintool/redis_data.html', template_data)



