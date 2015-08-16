[![Build Status](https://travis-ci.org/raviparekh/flask-error-handler.svg?branch=master)](https://travis-ci.org/raviparekh/flask-error-handler)

## Flask Error Handler

An alternative flask application error handler which attempts to provide an extensible and structured approach to exception handling 
for expected possible error scenario as well as the unexpected ones. 

As microservice architecture continues to being a popular choice for building systems, handling error among various interacting components in a concise way is important 
for support and debugging purposes.

### How to use:

View "demo" branch for example

Installing flask error handler:

    pip install flask_error_handler
    
Most components will have two categories of errors, this library categorises them into:

  1) Error category 
  
  2) Fatal Category 
 
The first category being error scenario, e.g. where a request was incorrect, this type of error are based on individual cases
and considered non critical to the health of the component.
The second category being fatal scenario, e.g. connection to database not being established, database is down, this probably is a show stopper for a component.

1) Therefore each component which requires error handling should create two sets of mapping, e.g.:


    ERROR_MESSSAGES = {
        'TEST_APP_ERR_001': 'Invalid user: request_data: $request_sent',
        'TEST_APP_ERR_002': 'some error calling system 1, URL called: $href and error message: $error_info'
    }
    
    FATAL_MESSAGES = {
        'TEST_APP_FATAL_000': 'Unknown system error has occurred',
        'TEST_APP_FATAL_002': 'Unable to connect to $href'
    }


2) From there continue to register the flask app to the error handler:


    app = Flask(__name__)
    register_app_for_error_handling(app.wsgi_app, "YOUR_APP_NAME", LOG)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run()

Now the entire flask application is wrapped by the error handler.

### Define your application exceptions
3) First define a root exception for your application which inherits the root exception from the library.
    

    class MyAppRootError(RootException):
        def __init__(self, app_err_code, status_code=500, **kwargs):
            #Passing the error mapping we defined for our application
            super(TestAppRootError, self).__init__(app_err_code, ERROR_MESSSAGES, FATAL_MESSAGES, status_code, **kwargs)

4) From there we can add more exceptions as the application grows, and add exception messages to the mapping we defined early.


     class InvalidRequestException(MyAppRootError):
        def __init__(self, app_err_code, **kwargs):
            super(InvalidRequestException, self).__init__(app_err_code, 400, **kwargs)


So now in the validation layer of the component, where we may perform request validation we can throw this exception:


     def is_user_valid(request):
        if(user_not_valid(request)):
            raise InvalidRequestException('TEST_APP_ERR_001', request_sent=request.json())
         #continue_with_execution

     
And the error handler will catch this exception being thrown higher up in the call stack, logs the exception and output an structured json to the client with the application error code, e.g.:
    
    {
        "logref": "some_generated_logref",
        "additional_info": "None",
        "error_message": "Invalid user: request_data: {'token': 1234, 'userId': 'user123' }",
        "app_err_code": "TEST_APP_ERR_001"
    }