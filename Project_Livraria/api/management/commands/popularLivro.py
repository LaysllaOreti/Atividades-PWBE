import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Livro
 
class Command(BaseCommand):
 
    def add_arguments(self, parser):
        parser.add_argument("--arquivo", default="Population/livros.csv")
        parser.add_argument("--truncate", action="store_true")
        parser.add_argument("--update", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        df = pd.read_csv(options["arquivo"], encoding="utf-8-sig")
        df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]
 
        if options["truncate"]: Livro.objects.all().delete()