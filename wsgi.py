import argparse
from app import create_app
from waitress import serve

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=8078, type=int, help="The port to listen the app"
    )
    args = parser.parse_args()
    app = create_app()
    serve(app=app, host="0.0.0.0", port=args.port)
