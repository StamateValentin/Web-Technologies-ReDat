import os
# os.system("pipenv shell")
import threading

from services.external.statistics.statistics import *

x = threading.Thread(target=general_up_votes_statistic, daemon=True)
y = threading.Thread(target=comments_statistic, daemon=True)
z = threading.Thread(target=upvote_ratio_statistic, daemon=True)
t = threading.Thread(target=ups_downs_statistic, daemon=True)
x.start()
y.start()
z.start()
t.start()
os.system(""
          "gunicorn services.proxy.main:app -b :8000 --reload | "  # PROXY
          "gunicorn services.auth.main:app -b :8001 --reload |"  # AUTHENTICATION
          "gunicorn services.external.main:app -b :8002 --reload"  # EXTERNAL
          "gunicorn services.server.main:app -b :8003 --reload"  # SERVER
          )

