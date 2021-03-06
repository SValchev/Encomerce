from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from payments.forms import UserForm, SigninForm, CardForm
from payments.models import User, UnpadaidUser
import django_ecommerce.settings as settings
import stripe
import datetime
import socket
from locale import currency

stripe.api_key = settings.STRIPE_SECRET

def soon():
    soon = datetime.date.today() + datetime.timedelta(days=30)
    return {'month':soon.month, 'year':soon.year }

def sign_in(request):
    user = None

    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            result = User.objects.filter(email=form.cleaned_data['email'])
            if len(result) == 1:
                if result[0].check_password(form.cleaned_data['password']):
                    request.session['user'] = result[0].pk
                    return HttpResponseRedirect('/')
                else:
                    form.addError("Incorect email or password")
            else:
                form.addError("Incorect email or password")
    else:
        form = SigninForm()

    print((form.non_field_errors()))

    return render_to_response(
        'payments/sign_in.html',
        {
            'form':form,
            'user':user
        },
        context_instance=RequestContext(request)
    )

def sign_out(request):
    del request.session['user']
    return HttpResponseRedirect('/')

def register(request):
    user = None
    if request.method == 'POST':
        print('-'*50)
        print(request.POST)
        print('-'*50)

        form = UserForm(request.POST['fraction'])
        print(form.is_valid())
        if form.is_valid():
            #update based on your billing method (subscription vs one time)
            # customer = Customer.create(
            #     email=form.cleaned_data['email'],
            #     description=form.cleaned_data['name'],
            #     card=form.cleaned_data['stripe_token'],
            #     plan="gold",
            # )
            customer = stripe.Charge.create(
                description=form.cleaned_data['email'],
                card={
                    'number': '4242424242424242',
                    'exp_month': 10,
                    'exp_year': 2016
                    },
                amount="5000",
                currency="usd"
            )

            cd = form.cleaned_data

            from django.db import transaction

            try:
                with transaction.atomic():
                    user = User.create(name=cd['name'], email=cd['email'], password=cd['password'],
                                       last_4_digits=cd['last_4_digits'], fraction=request.POST['fraction'], stripe_id="")
                    if customer:
                        user.stripe_id = customer.id
                        user.save()
                    else:
                        UnpaidUsers(email=cd['email']).save()

            except IntegrityError:
                import traceback
                form.addError(cd['email'] + ' is already a member' +
                              traceback.format_exc())
                user = None
            else:
                request.session['user'] = user.pk
                return HttpResponseRedirect('/')

    else:
        form = UserForm()

    return render_to_response(
        'payments/register.html',
        {
            'form': form,
            'months': list(range(1, 12)),
            'publishable': settings.STRIPE_PUBLISH,
            'soon': soon(),
            'user': user,
            'years': list(range(2011, 2036)),
        },
        context_instance=RequestContext(request)
    )

def edit(request):
    uid = request.session.get('user')

    if uid is None:
        return HttpResponseRedirect('/')

    user = User.objects.get(pk=uid)

    if request.method == 'POST':
        form=CardForm(request.POST)
        if form.is_valid():

            customer=stripe.Customer.retrieve(user.stripe_token)
            customer.card = form.cleaned_data['stripe_token']
            customer.save()

            user.last_4_digits = form.cleaned_data['last_4_digits']
            user.stripe_token = customer.id
            user.save()

            return HttpResponseRedirect('/')

        else:
            form=CardForm()

        return render_to_response(
            'payments/edit.html',
            {
                'form':form,
                'publishable':settings.STRIPE_PUBLISH,
                'soon':soon(),
                'months':list(range(1,12)),
                'years':list(range(2011,2036)),
            },
            context_instance=RequestContext(request)
        )


class Customer(object):
    @classmethod
    def create(cls, billing_method="subscritpion", **kwargs):
        try:
            if billing_method == "subscritpion":
                return stripe.Customer.create(**kwargs)
            elif billing_method == "one_time":
                return stripe.Charge.craete(**kwargs)
        except socket.error:
            return None
