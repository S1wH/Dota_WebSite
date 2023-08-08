import time
from django_rq import job
from .models import Author


@job
def get_report():
    start = time.time()
    time.sleep(60)
    authors = Author.objects.all()
    with open('report.txt', 'w', encoding='utf-8') as f:
        for author in authors:
            f.write(author.nickname+'\n')
    return time.time() - start


@job
def get_report_fast():
    time.sleep(5)
    authors = Author.objects.all()
    with open('report_fast.txt', 'w', encoding='utf-8') as f:
        for author in authors:
            f.write(author.nickname+'\n')
