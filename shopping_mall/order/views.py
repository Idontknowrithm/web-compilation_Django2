from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from user.decorators import login_required
from .forms import RegisterForm
from .models import Order

# Create your views here.

@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    # form view를 화면을 보여주는 용도로 사용하지 않으니 template_name은 필요없음
    # template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'
    
    # form 전달이 실패했을 때 같은 페이지로 리다이렉트
    def form_invalid(self, form):
        return redirect('/product/' + str(form.product))
    
    # form을 전달할 때 어떤 인자값을 보낼 것인 지 결정
    def get_form_kwargs(self, **kwargs):
        # kw에 기존 인자값을 저장
        kw = super().get_form_kwargs(**kwargs)
        # kw에 request 인자값을 추가해서 저장
        kw.update({
            'request': self.request
        })
        return kw

@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order_list'
    
    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(user__email=self.request.session.get('user'))
        return queryset