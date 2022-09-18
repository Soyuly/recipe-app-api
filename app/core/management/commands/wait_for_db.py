"""
Django command to wait for the database to be availiable
"""
import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django comand to wait for database."""

    def handle(self, * args, **options):
        "Entrypoint for command."
        self.stdout.write("Waiting for database")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database unavailabe, waiting 1 seconds...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('DATABASE available!!'))
