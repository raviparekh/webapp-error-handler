from run_server import create_app

application = create_app()
application.config['PROPAGATE_EXCEPTIONS'] = True

