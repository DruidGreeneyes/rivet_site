from django.db import models

# Create your models here.


def _first_chars(text, num=60):
    return text[:num]


class Comparison(models.Model):
    document_a = models.TextField()
    document_b = models.TextField()
    result = models.FloatField()

    def str(self):
        doc_a = _first_chars(self.document_a)
        doc_b = _first_chars(self.document_b)
        res = self.result
        return "{}... <?> {}... = {}".format(doc_a, doc_b, res)

    def __str__(self):
        return self.str()
