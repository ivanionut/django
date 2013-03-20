import urllib2
from django import forms
#from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.utils.simplejson.decoder import JSONDecoder
from models import *


class WikisearchForm(forms.Form):
	autore = forms.IntegerField(widget=forms.Select(choices = [(autore.pk, autore) for autore in Autore.objects.all()]))
	wikipedia = forms.CharField(widget=forms.Select(choices=(("it","Italiana"),("en","Inglese"))))
	limite = forms.IntegerField(initial=10,widget=forms.RadioSelect(choices=((10,"10"),(50,"50"),(100,"100"))))
	
	# funzione per la verifica di un campo, al momento commentata
	# def clean_limite(self):
		# if (self.cleaned_data['limite'] > 50 and self.cleaned_data['wikipedia'] == 'en'):
			# raise forms.ValidationError("Massimo 50 risultati in inglese!")
		# return self.cleaned_data['limite']
	
wiki_url_api="http://%s.wikipedia.org/w/api.php?action=query&format=json&srlimit=%s&list=search&srsearch=%s"
wiki_link="http://%s.wikipedia.org/wiki/"


def ricerca(request):
	risultati = link = None
	if request.method == 'POST':
		form = WikisearchForm(request.POST)
		if form.is_valid():
			autore = get_object_or_404(Autore,pk=form.cleaned_data['autore'])
			url = wiki_url_api % (form.cleaned_data['wikipedia'],form.cleaned_data['limite'],autore.cognome)
			link = wiki_link % form.cleaned_data['wikipedia']
			dati = urllib2.urlopen(url.encode('utf-8')).read()
			valori = JSONDecoder().decode(dati)
			risultati = valori['query']['search']
	else:
		form = WikisearchForm()
	c = {
	'form': form,
	'link': link,
	'risultati': risultati,}
	c.update(csrf(request))
	return render_to_response('wikisearch.html', c)