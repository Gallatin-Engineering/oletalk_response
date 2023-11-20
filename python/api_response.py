 
# =================================================================================== 
#    COPYRIGHT (&copy) 2020-2023 GALLATIN ENGINEERING LTD. ALL RIGHTS RESERVED.
# -----------------------------------------------------------------------------------
#    THE FOLLOWING SOURCE CODE IS THE EXCLUSIVE PROPERTY OF GALLATIN ENGINEERING LTD 
#    AND SHOULD NOT BE COPIED, SHARED, DISTRIBUTED OR REDISTRIBUTED, WITHOUT THE 
#    EXPRESSED CONSENT OF GALLATIN ENGINEERING LTD. THE SOURCE CODE CAN ONLY BE 
#    USED IN ACCORDANCE WITH THE ACCOMPANYING LICENSE FILE INCLUDED IN THE SOURCE 
#    CODE PACKAGE. IN THE ABSENCE OF SUCH LICENSE DOCUMENT, ONLY THE ABOVE 
#    RESTRICTIONS ARE ENFORCED AND MUST BE STRICTLY ADHERED TO.
# ===================================================================================


# """Lambda Layer:    'Cross-function library for inter AWS Lambda, and Client <--> API communications.'   \n
# @Application:       'N/A'       \n
# @Package:           'None'  \n
# @Module:            'api_response'           \n   
# @Description:       'Python File (module) that contains the functions necessary to generate HTTP responses.    \n
# @AUTHOR/PROGRAMMER: muddicode/sauceCode                 \n
# @VERSION:           4.0.0 - Added Features: (@TODO: )    \n
# USAGE:              'Used for client/server messaging over the internet, eg: Mobile . All communications to and from APIs are in this form.'  \n
# CHANGELOG:          Add a 'html response' function that cleans up the code and no need to 
#                     call a different function for 'html' (website) operations.
# """


"""
PACKAGE:
========
    oletalk_response

Module: 
-------
    api_response

Classes:
--------
    None.
    
Functions:
----------
    respond
    html_response
    error_response
    lambda_response

Exceptions:
-----------
    None.
    
"""


import json
from pprint import pprint
from time import ctime

    
def lambda_response(status_code, message, **kwargs) -> dict:
    '''Presents the custom OleTalk API Gateway/server responses in standard HTTP format, for all communications sent
    from the API to the client.    \n
    
    Parameters:
    -----------    
        status_code (int, req'd):
            Standard http codes.    \n
            
        msg (str, req'd):
            String displaying the message response. \n 
            
        kwargs (dict, opt):
            Other relevant data (used in debugging) such as Exceptions, etc.    \n
      
    Returns:
    --------
        return (dict):
            Response to the client's requests in standard HTTP form.  \n
    
    ''' 
    data = {"message": message}
    for key in kwargs:
        data.update({key: kwargs[key]})
    return {   
        'statusCode': status_code,     #   cCode, sCode, conf_cde, stat_cde
        'body': json.dumps(data)
    }  
   
    
    
def html_response(status_code, html) -> dict:
    '''Responds with html (or web page) as its payload instead of a json object.    \n
    
    Parameter:
    ----------
        status_code (int/str, req):
            Standard HTTP Status Codes.     \n
            
        html (txt, req.): 
            HTML formatted text.    \n
    
    Returns:
    --------
        return (dict, req):
            A response with HTML formatted text in the body.  \n

    '''
    return {
        "headers": {
            "Content-Type": "text/html"
        },
        "statusCode": status_code,
        "body": html
    }    
    
def error_response(error_code, error_message, **kwargs) -> dict:
    '''Presents the Error in the required standard format, 
    or all error communications from the API to the client.    \n
    
    Parameters:
    -----------
        error_code (int, req'd):
            HTTP Status/Error code for this error-type.    \n
            
        error_message (str, req'd):
            HTTP code for the error.    \n
            
        kwargs (dict, opt):
            The error details in key - value pairs giving further eg. stack trace, error type etc.    \n
        
    Returns:
    --------
        return (dict):
            Error presented in the standard HTTP response format.  \n
        
        '''
    #   should trigger logging and custom debugging functions.
    error_data = kwargs
    error_data.update({"errorMessage": error_message})
    error_data.update({"timestamp": ctime()})
    return {   
        'statusCode': error_code,           #   usually 400 or 500  follows the same convention as http error codes  \n
        'body': json.dumps(error_data)      #   including the 'call stack'
    } 
    
#   
    
def respond(err=None, res=None, html=None) -> dict:
    '''Customizes response using a consistant, standard format for AWS API Gateway/AWS Lambda Functions.     \n     
    
    Parameters:
    -----------
        err (exception/error object, opt): 
            Exception class based object. Must be set to None if not used.   \n
            
        res (dict, opt):
            Key-Value pairs containing the data being sent to a client.     \n
            
        html (text, opt):
            HTML formatted text.    \n    
            
    Returns:
    --------
        return (dict):
            Custom OleTalk API response in the standard http format.
    
    '''
    return {
        "headers": {
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Methods": 'GET,POST,OPTIONS',
            "Access-Control-Allow-Headers": 'Content-Type',
            # "Content-Type": "text/html" if html else "application/json"
            "Content-Type": "text/html" if html else "application/json"
        },
        "statusCode": '400' if err else '200',
        "body": err if err else html if html else json.dumps(res)
    }

