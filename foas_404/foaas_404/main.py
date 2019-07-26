#!/usr/bin/env python3
# pylint: disable = C0103
'''
This will pull a random "Fuck off as a service" request from the
https://foaas.com/ website API, and insert variables as needed for the
API request to be returned as a custom 404 page.

:return: foas_404 and page template

:requirements: pip install foaas; wsgi
'''
import os
import random
from flask import Flask
import foaas


app = Flask(__name__)


def template():
    '''
    Formatting template for web page.
    '''
    page_template = '''
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <title>404 - Get Fucked</title>
  </head>
  <body>
  <div class="p-4 container-fluid">
    <h1>404 - Get Fucked</h1><br>
    {}
    </div>
    <br>
    <br>
  </body>
</html>
'''
    return page_template


def get_fucked():
    '''
    Function name says it all.
    '''
    name = ['Alucard', 'Simon Belmont', 'Dracula', 'Carmilla']
    f_name = random.choice(name)
    t_name = random.choice(name)
    f = foaas.Fuck()

    fucked = f.random(name=t_name, _from=f_name)

    return fucked


@app.route("/")
def fucking_return():
    '''
    Web application home page.
    '''
    fuck_you = get_fucked()

    return template().format(fuck_you)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 6787))
    app.run(host='0.0.0.0', port=PORT)
