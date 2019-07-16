"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

import traceback


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    page = """
        <head>
            <title>WSGI Calculator: Add</title>
        </head>
        """
    if len(args) == 2:
        total = sum(map(int, args))
        return page + 'Adding {} + {} <br>Your total is: {}<br><br><a href="http://localhost:8080">Home</a>'.format(str(args[0]), str(args[1]), str(total))
    else:
        return page + 'Please, enter exactly 2 arguments.<br><br><a href="http://localhost:8080">Home</a>'


def subtract(*args):
    """ Returns a STRING with the subtraction of the arguments """
    page = """
        <head>
            <title>WSGI Calculator: Subtract</title>
        </head>
        """
    if len(args) == 2:
        total = int(args[0]) - int(args[1])
        return page + 'Subtracting {} - {}<br>Your total is: {}<br><br><a href="http://localhost:8080">Home</a>'.format(str(args[0]), str(args[1]), str(total))
    else:
        return page + 'Please, enter exactly 2 arguments.<br><br><a href="http://localhost:8080">Home</a>'


def multiply(*args):
    """ Returns a STRING with the multiplication of the arguments """
    page = """
        <head>
            <title>WSGI Calculator: Multiply</title>
        </head>
        """
    if len(args) == 2:
        total = int(args[0]) * int(args[1])
        return page + 'Multiplying {} x {}<br>Your total is: {}<br><br><a href="http://localhost:8080">Home</a>'.format(str(args[0]), str(args[1]), str(total))
    else:
        return page + 'Please, enter exactly 2 arguments.<br><br><a href="http://localhost:8080">Home</a>'


def divide(*args):
    """ Returns a STRING with the division of the arguments """
    page = """
        <head>
            <title>WSGI Calculator: Divide</title>
        </head>
        """
    if len(args) == 2:
        if int(args[1]) == 0:
            return page + 'Divide by zero attempt. <br><br><a href="http://localhost:8080">Home</a>'
        else:
            total = int(args[0]) / int(args[1])
            return page + 'Dividing {} / {}<br>Your total is: {}<br><br><a href="http://localhost:8080">Home</a>'.format(str(args[0]), str(args[1]), str(total))
    else:
        return page + 'Please, enter exactly 2 arguments.<br><br><a href="http://localhost:8080">Home</a>'


def home():
    page = """
        <head>
            <title>WSGI Calculator</title>
            <style>
                table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
                }
                th, td {
                padding: 15px;
                }
            </style>
        </head>
        <h1>Welcome to the WSGI Calculator</h1>
        <h2>See instructions below</h2>
        <table>
            <tr><th>Operation</th><th>Instructions</th><th>Example</th></tr>
            <tr><td>Add</td><td>/add/operand_1/operand_2</td><td><a href='http://localhost:8080/add/23/42'>http://localhost:8080/add/23/42</a></td></tr>
            <tr><td>Subtract</td><td>/add/operand_1/operand_2</td><td><a href='http://localhost:8080/subtract/23/42'>http://localhost:8080/subtract/23/42</a></td></tr>
            <tr><td>Multiply</td><td>/add/operand_1/operand_2</td><td><a href='http://localhost:8080/multiply/23/42'>http://localhost:8080/multiply/23/42</a></td></tr>
            <tr><td>Divide</td><td>/add/operand_1/operand_2</td><td><a href='http://localhost:8080/divide/23/42'>http://localhost:8080/divide/23/42</a></td></tr>
        </table>
        
        """
    return page


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    #  examples provide the correct *syntax*, but you should
    #  determine the actual values of func and args using the
    #  path.
    #  func = add
    #  args = ['25', '32']

    funcs = {
        '': home,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        }

    path = path.strip('/').split('/')

    func_name = path[0]

    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    #  work here as well! Remember that your application must
    #  invoke start_response(status, headers) and also return
    #  the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    #  to divide by zero.
    headers = [('Content-type', 'text/html')]

    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError

        func, args = resolve_path(path)
        
        body = func(*args)
        status = '200 OK'

    except NameError:
        status = '404 Not Found'
        body = '<h1>Not Found</h1>'

    except Exception:
        status = '500 Internal Server Error'
        body = '<h1>Internal Server Error</h1>'
        print(traceback.format_exc())

    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':

    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
