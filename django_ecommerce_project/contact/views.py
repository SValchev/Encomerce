# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from .forms import ContactView
from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        print(request.POST)
        form = ContactView(request.POST)
        print(form.is_valid())
        if form.is_valid():
            our_form = form.save(commit=False)
            our_form.save()
            messages.add_message(
                                 request,
                                 messages.INFO,
                                 'Your message has been sent thank you!')

            return HttpResponseRedirect('/')
    else:
        form = ContactView()

    t = loader.get_template('contact/contact.html')
    c = RequestContext(request, {'form':form},)

    return HttpResponse(t.render(c))
