from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Comparison

from pyrivet_core.sqlite3_lexicon import Lexicon
from pyrivet_core import rivet

# Create your views here.


def get_latest_comparisons(num=5):
    return Comparison.objects.order_by('id')[:num]


def index(request):
    latest_comparisons = get_latest_comparisons()
    context = {
        'latest_comparisons': latest_comparisons,
    }
    output = render(request, 'rivet/index.html', context)
    return output


def submit(request):
    try:
        document_a, document_b = sorted((request.POST['doca'], request.POST['docb']))
    except KeyError:
        latest_comparisons = get_latest_comparisons()
        return render(request, 'rivet/index.html', {
            'latest_comparisons': latest_comparisons,
            'error_message': "Bad Input!"
        })
    else:
        try:
            cmp = Comparison.objects.get(document_a=document_a, document_b=document_b)
        except Comparison.DoesNotExist:
            print("Comparing documents: ")
            with Lexicon.open(size=1000, nnz=8) as lexicon:
                result = rivet.compare_documents(document_a, document_b, lexicon=lexicon, ingest=True)
                result = result[0][1]
            cmp = Comparison(document_a=document_a, document_b=document_b, result=result)
            cmp.save()
        return HttpResponseRedirect(reverse('comparison', args=(cmp.id,)))


def comparison(request, comparison_id):
    c = get_object_or_404(Comparison, pk=comparison_id)
    return render(request, 'rivet/comparison.html', {'comparison': c})



