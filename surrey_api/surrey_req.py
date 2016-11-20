import requests
import json
import re
import os
import time

API_ENDPOINT = "http://cosmos.surrey.ca/api/open311"

"""
Get a list of all service definitions

@return Request object
"""
def get_service_list():
    payload = {'jurisdiction_id': 'surrey.ca'}
    resource = API_ENDPOINT + "/services.json"
    return requests.get(resource, params=payload)


"""
Get a definition of a service by service_code

@param service_code: code of a particular service defined by API
@return Request object

Note: see http://cosmos.surrey.ca/api/open311/services.{xml,json} for service definitions
"""
def get_service_def(service_code):
    payload = {'jurisdiction_id': 'surrey.ca'}
    resource = API_ENDPOINT + "/services/" + str(service_code) + ".json"
    return requests.get(resource, params=payload)


"""
Get a list of all requests within a 1 day default time limit

@param start_date: beginning of request time frame
@param end_date: end of request time frame
@param status: OPEN or closed
@return Request object

Note: Time format: 2010-05-24, will throw ValueError otherwise
"""
def get_all_requests(start_date="", end_date="", status="OPEN"):

    # an empty service_code is required in the URL (bug?)
    payload = {'jurisdiction_id': 'surrey.ca', 'service_code': ''}

    if start_date == "" or end_date == "":
        curr_time   = time.time()
        time_format = "%Y-%m-%d"
        start_date  = time.strftime(time_format, time.gmtime(curr_time - 60*60*24))
        end_date    = time.strftime(time_format, time.gmtime(curr_time))
    else:
        time_match = re.compile(r'^2[0-9]{3}(-[0-9]{2}){2}$')
        if not time_match.match(start_date) or not time_match.match(end_date):
            raise ValueError("Time is not formatted properly.")

    payload['start_date']   = start_date
    payload['end_date']     = end_date
    payload['status']       = status

    resource = API_ENDPOINT + "/requests.json"
    return requests.get(resource, params=payload)


"""
Get a request by service_request_id

@param service_request_id: id of a particular request
@return Request object
"""
def get_request_by_id(service_request_id):
    payload = {'jurisdiction_id': 'surrey.ca'}
    resource = API_ENDPOINT + "/requests/" + str(service_request_id) + ".json"
    return requests.get(resource, params=payload)




if __name__ == "__main__":

    if not os.access('./data/', os.F_OK):
        os.mkdir('./data/')

    # Get all data from 2010-01-01 to today
    # NOTE: if time is > 2016, change last 2 steps and loop range accordingly
    for i in range(6):
        year = '201{}'.format(i)
        fname = './data/requests_'+year+'0101_'+year+'1231_CLOSED.json'
        res = get_all_requests(start_date=year+"-01-01",end_date=year+"-12-31",status="CLOSED")
        print fname
        print res.url
        with open(fname,'w') as f:
            json.dump(res.json(), f)

    today_compact = time.strftime("%Y%m%d",time.localtime(time.time()))
    today_hyphen  = time.strftime("%Y-%m-%d",time.localtime(time.time()))

    curr_open_fname = './data/requests_20160101_'+today_compact+'_OPEN.json'
    curr_closed_fname = './data/requests_20160101_'+today_compact+'_CLOSED.json'
    with open(curr_open_fname,'w') as f:
        res = get_all_requests(start_date="2016-01-01",end_date=today_hyphen)
        print curr_open_fname
        print "Response code: {}".format(res.status_code)
        print res.url
        json.dump(res.json(), f)

    with open(curr_closed_fname,'w') as f:
        res = get_all_requests(start_date="2016-01-01",end_date=today_hyphen, status="CLOSED")
        print curr_closed_fname
        print "Response code: {}".format(res.status_code)
        print res.url
        json.dump(res.json(), f)
