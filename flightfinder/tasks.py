from datetime import datetime, timedelta
import time
from flightfinder.lib.merlin import Merlin
from flightfinder.models import CachePath
from pathfinder.celery import app


@app.task
def cache_flights():

    paths_to_cache = CachePath.objects.all()
    for path in paths_to_cache:
        # Iterate over the next 14 days
        for day in range(14):

            date = datetime.now() + timedelta(days=day)
            formatted_date = date.strftime("%d.%m.%Y")

            # Summon Merlin with the date for the current iteration
            merlin = Merlin(path.origin.code, path.destination.code, formatted_date)

            # Perform magic
            merlin.prepare_magic()
            merlin.abracadabra()
            merlin.persist_magic()

            # Delay for 1 minute after each iteration
            time.sleep(90)


app.conf.beat_schedule = {
    "run-cache-flights-every-12-hours": {
        "task": "flightfinder.tasks.cache_flights",
        "schedule": timedelta(hours=12),
    },
}
app.conf.timezone = "UTC"
