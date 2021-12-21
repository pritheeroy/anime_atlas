"""
Flask app for handling server requests
"""
import python_ta
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def start() -> str:
    """Prints init message on local host once flask app is started.

    Precondition:
        - Nothing is running on 127.0.0.1:5000 already.
    """

    return 'Initialized!'


@app.route('/anime-atlas')
def content() -> str:
    """
    Prints success message once authorization is completed.
    Generates txt file with Authorization Code required for token generation.

    Preconditions:
        - Authentication URL has been succesfully generated.
        - Successful authorization has occurred and a user has logged into their MAL account.
    """

    user = request.args.get('code')
    # file = open("code.txt", "r+")
    # file.truncate(0)
    # file.close()
    file = open('code.txt', 'w')
    file.write(user)
    file.close()
    return 'Success! Return to Application!'
    # return user


def shutdown_server() -> None:
    """
    Ends current server on local host completely. Must run myapp again to restart it.

    Preconditions:
        - myapp.py has already been running
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['GET'])
def shutdown() -> str:
    """Uses built in flask method to shut down server while providing confirmation on local host

    Preconditions:
        - myapp.py has already been running
    """
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run()
#     python_ta.check_all(config={
#         'extra-imports': [],  # the names (strs) of imported modules
#         'allowed-io': [],  # the names (strs) of functions that call print/open/input
#         'max-line-length': 100,
#         'disable': ['E1136']
#     })
