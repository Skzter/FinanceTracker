from django.db import models
from datetime import datetime

# Create your models here.
class Ausgaben(models.Model):
    TYPE = (
        ('E', 'Einnahmen'),
        ('A', 'Ausgaben')
    )
    MONTHS = (
        (1, 'Januar'),
        (2, 'Februar'),
        (3, 'März'),
        (4, 'April'),
        (5, 'Mai'),
        (6, 'Juni'),
        (7, 'Juli'),
        (8, 'August'),
        (9, 'September'),
        (10, 'Oktober'),
        (11, 'November'),
        (12, 'Dezember'),
    )

    CATEGORYS = (
        ('W', 'Wohnen'),
        ('L', 'Leben'),
        ('H/F', 'Hobby/Freizeit'),
        ('M', 'Mobilität'),
        ('B', 'Bildung'),
        ('S/I', 'Sparen/Investieren'),
        ('S', 'Sonstiges')
    )

    type = models.CharField(
        max_length=1,
        choices=TYPE,
        default='A',
        help_text="Einnahme oder Ausgabe."
    )
    month = models.IntegerField(
        choices=MONTHS,
        default=MONTHS[datetime.now().month-1],
        help_text="Monat der Ausgabe."
    )
    category = models.CharField(
        max_length=10,
        choices=CATEGORYS,
        help_text="Kategorie der Ausgabe."
    )
    title = models.CharField(max_length=30, help_text="Bezeichnung der Ausgabe.")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Betrag der Ausgabe.")


    def __str__(self):
        return f"{self.type}-{self.title}: {self.amount}"
