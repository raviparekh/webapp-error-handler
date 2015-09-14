## Flask Error Handler
Quick Demo example created of using flask error handler.

How to get started:


    pip install -r requirements.txt


And to run locally:
    
    python run_server.py

Application to start at address: http://127.0.0.1:5000

Example of response when authentication fails:

    {
        "logref": "4bfc1ede441011e58522001e0b80fbe8",
        "additional_info": {
            "more_info": "contact support"
        },
        "error_message": "Authorisation error, incorrect login details for user1",
        "app_err_code": "ERR_001"
    }