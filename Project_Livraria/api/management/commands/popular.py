import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Autor
 
class Command(BaseCommand):
 
    def add_arguments(self, parser):
        parser.add_argument("--arquivo", default="Population/autores.csv")
        parser.add_argument("--truncate", action="store_true")
        parser.add_argument("--update", action="store_true")
 
    @transaction.atomic
    def handle(self, *args, **options):
        df = pd.read_csv(options["arquivo"], encoding="utf-8-sig")
        df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]
 
        if options["truncate"]: Autor.objects.all().delete()
 
        df["nome"] = df["nome"].astype(str).str.strip()
        df["sobrenome"] = df["sobrenome"].astype(str).str.strip()
        df["data_nascimento"] = pd.to_datetime(df["data_nascimento"], errors="coerce", format="%Y-%m-%d").dt.date
        df["nacao"] = df.get("nacao", "").astype(str).str.strip().str.capitalize().replace({"":None})
   
        df = df.query("nome != '' and sobrenome != '' ")
        df = df.dropna(subset='data_nascimento')
 
        if options["update"]:
            criados = atualizados = 0
            for row in df.itertuples(index=False):
                _, created = Autor.objects.update_or_create(
                    nome = row.nome,
                    sobrenome = row.sobrenome,
                    data_nascimento = row.data_nascimento,
                    defaults={"nacao": row.nacao}
                )
 
                criados += int(created)
                atualizados += int(not created)
           
            self.stdout.write(self.style.SUCCESS(f"Criados: {criados}\nAtualizados: {atualizados}"))
        else:
            objs = [Autor(
                    nome = row.nome,
                    sobrenome = row.sobrenome,
                    data_nascimento = row.data_nascimento,
                    nacao = row.nacao
            ) for row in df.itertuples(index=False)]
           
            Autor.objects.bulk_create(objs, ignore_conflicts=True)
 
            self.stdout.write(self.style.SUCCESS(f"Criados: {len(objs)}"))
 