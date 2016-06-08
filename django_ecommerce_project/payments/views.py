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

stripe.api_key=settings.STRIPE_SECRET

def soon():
    soon = datetime.date.today() + datetime.timedelta(days=30)
    return {'month':soon.month, 'year':soon.year }


def sign_in(request):
    user = None

    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            result=User.objects.filter(email=form.cleaned_data['email'])
            if len(result) == 1:
                if result[0].check_password(form.cleaned_data['password']):
                    return HttpResponseRedirect('/')
                else:
                    form.add_error("Incorect email or password")
            else:
                form.add_error("Incorect email or password")
    else:
        form = SigninForm()

    print((form.non_field_errors()))

    return render_to_response('payments/sign_in.html',{'form':form, 'user':user}, context_instance=RequestContext(request))


def sign_out(request):
    del request.session['user']
    return HttpResponseRedirect('/')


def register(request):
    user = None
    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            customer = stripe.Customer.create(
                 email=form.cleaned_data['email'],
                 description=form.cleaned_data['name'],
                 card=form.cleaned_data['stripe_token'],
                 plan='gold',
             )

            # custerm = stripe.Charge.create(
            #      description=form.cleaned_data['email'],
            #      card=form.cleaned_data['stripe_token'],
            #      amount='5000',
            #      currency='usd',
            # )

            cd = form.cleaned_data

            try:
                user = User.create(
                    name=cd['name'],
                    email=cd['email'],
                    last_4_digits=cd['last_4_digits'],
                    stripe_id='',
                    password=cd['password']
                )

                if customer:
                    user.stripe_id = customer.id
                    user.save()
                else:
                    UnpadaidUser(email=cd['email']).save()

            except IntegrityError:
                form.add_error(cd['email'] + " is already a mamber!")
                user = None
            else:
                request.session['user']=user.pk
                return HttpResponseRedirect('/')

    else:
        form = UserForm()

    return render_to_response(
            'payments/register.html',
            {
             'form':form,
             'months':list(range(1,12)),
             'publishable':settings.STRIPE_PUBLISH,
             'soon':soon(),
             'user':user,
             'years':list(range(2011,2036)),
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
