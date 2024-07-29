from datetime import datetime, timedelta
import time
from flightfinder.lib.merlin import Merlin
from flightfinder.models import CachePath
from pathfinder.celery import app

import logging

logger = logging.getLogger(__name__)


@app.task
def cache_flights():
    # print("Caching flights")
    logger.debug("Caching flights")
    paths_to_cache = CachePath.objects.all()
    for path in paths_to_cache:
        # Iterate over the next 14 days
        for day in range(14):

            try:
                date = datetime.now() + timedelta(days=day)
                formatted_date = date.strftime("%d.%m.%Y")

                # Summon Merlin with the date for the current iteration
                merlin = Merlin(path.origin.code, path.destination.code, formatted_date)

                # Perform magic
                merlin.prepare_magic()
                merlin.abracadabra()
                merlin.persist_magic()

                # Delay for 5 seconds after each iteration
                time.sleep(5)
            except Exception as e:
                logger.debug("Error running cache flights: %s", e)
                continue


app.conf.beat_schedule = {
    "run-cache-flights-every-4-hours": {
        "task": "flightfinder.tasks.cache_flights",
        "schedule": timedelta(hours=4),
    },
}
app.conf.timezone = "UTC"

# Manually trigger the task to run immediately
cache_flights.apply_async()
