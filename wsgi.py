import os
from dotenv import load_dotenv

from interface import create_app, scheduler, appInster, db
from interface.interprints.apscheduler import registerAllTask

if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    app = create_app('development')
    app.app_context().push()
    scheduler.init_app(app=app)

    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        scheduler.api_enabled = True
        scheduler.init_app(app=app)
        registerAllTask()
        scheduler.start()
    app.run(host="0.0.0.0", port=8080)
