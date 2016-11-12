import re
import json
import time
import math
import calendar
import operator
from collections import Counter

import surrey_req

"""
Requests responses have the form:

[
  {
    "service_request_id":638344,
    "status":"closed",
    "status_notes":"Duplicate request.",
    "service_name":"Sidewalk and Curb Issues",
    "service_code":006,
    "description":null,
    "agency_responsible":null,
    "service_notice":null,
    "requested_datetime":"2010-04-14T06:37:38-08:00",
    "updated_datetime":"2010-04-14T06:37:38-08:00",
    "expected_datetime":"2010-04-15T06:37:38-08:00",
    "address":"8TH AVE and JUDAH ST",
    "address_id":545483,
    "zipcode":94122,
    "lat":37.762221815,
    "long":-122.4651145,
    "media_url":"http://city.gov.s3.amazonaws.com/requests/media/638344.jpg "
  },
]

"""

def service_distribution(json_fp):
    with open(json_fp, 'r+') as f:
        requests = json.load(f)

    cnt = Counter()
    for req in requests:
        cnt[req['service_code']] += 1

    return cnt


def agency_distribution(json_fp):
    with open(json_fp, 'r+') as f:
        requests = json.load(f)

    cnt = Counter()
    for req in requests:
        cnt[req['agency_responsible']] += 1

    return cnt


def num_requests(json_fp):
    cnt = service_distribution(json_fp)
    return sum(cnt.values())


def avg_close_time(json_fp):
    with open(json_fp, 'r+') as f:
        requests = json.load(f)

    completion_time_arr = []
    avg_completion_time = 0
    no_update_time      = 0
    no_expected_time    = 0

    for req in requests:
        if req['updated_datetime'] == "" and req['expected_datetime'] == "":
            no_expected_time += 1
            no_update_time += 1
            continue
        if req['updated_datetime'] == "":
            no_update_time += 1
            continue
        if req['expected_datetime'] == "":
            no_expected_time += 1

        start_time  = req['requested_datetime'].replace('-08:00', '')
        end_time    = req['updated_datetime'].replace('-08:00', '')

        try:
            start_time  = calendar.timegm(time.strptime(start_time, '%Y-%m-%dT%H:%M:%S'))
            end_time    = calendar.timegm(time.strptime(end_time, '%Y-%m-%dT%H:%M:%S'))
        except ValueError:
            print "start_time error: {0}".format(start_time)
            print "end_time error: {0}".format(end_time)
            continue

        # Someone goof'd when inputting times...
        if start_time > end_time:
            temp = start_time
            start_time = end_time
            end_time = start_time

        completion_time_arr.append(end_time - start_time)

    return completion_time_arr, no_update_time, no_expected_time

def variance_close_times(times_arr, avg_of_arr):
    return sum(map(lambda x: (x - avg_of_arr)**2, times_arr)) / len(times_arr)

def pretty_print_dist(dist_dict):
    max_spaces = len(max(dist_dict.keys(), key=len)) + 3
    max_value  = max(dist_dict.values())
    sum_values = sum(dist_dict.values())
    sorted_dist_dict = sorted(dist_dict.items(), key=operator.itemgetter(1), reverse=True)
    service_keys = surrey_req.get_service_list().json()
    for tup in sorted_dist_dict:
        num_spaces      = max_spaces - len(tup[0])
        num_bars        = int((tup[1] / float(max_value)) * 50) + 1
        pcnt_of_total   = " ("+str(round(tup[1] / float(sum_values),3))+")"
        print str(tup[0])+":"+(" "*num_spaces)+("|"*num_bars)+"  "+str(tup[1])+pcnt_of_total


if __name__ == "__main__":

    req_open_fp = "./data/requests_20160101_20161112_OPEN.json"
    req_closed_fp = "./data/requests_20160101_20161112_CLOSED.json"

    all_closed      = num_requests(req_closed_fp)
    compl_time_arr, no_close, no_expected = avg_close_time(req_closed_fp)
    num_zeros        = Counter(compl_time_arr)[0]

    avg_comp_time   = sum(compl_time_arr) / len(compl_time_arr)
    var_comp_time   = variance_close_times(compl_time_arr, avg_comp_time)
    avg_hours       = (avg_comp_time)/3600
    avg_minutes     = ((avg_comp_time)%3600)/60
    var_hours       = int((var_comp_time))/3600
    var_minutes     = (int((var_comp_time))%3600)/60
    sdev_hours      = int(math.sqrt(var_comp_time))/3600
    sdev_minutes    = (int(math.sqrt(var_comp_time))%3600)/60

    print "\n======================================================="
    print "                     REQUESTS REPORT                     "
    print "=======================================================\n"
    print "Num total req:                         {0} (%100)".format(all_closed)
    print "Req with no close time:                {0} (%{1})".format(no_close, round(no_close/float(all_closed),2))
    print "Req with no expected close time:       {0} (%{1})".format(no_expected, round(no_expected/float(all_closed),2))
    print "Num requests serviced in 0 time:       {0} (%{1})\n".format(num_zeros, round(num_zeros/float(all_closed),2))
    print """Extremes:                         MIN: {0}
                                  MAX: {1}\n""".format(min(compl_time_arr), max(compl_time_arr))
    print """Avg time to close req:          HOURS: {0}
                                  MIN: {1}\n""".format(avg_hours, avg_minutes)
    print """Var time to close req:          HOURS: {0}
                                  MIN: {1}\n""".format(var_hours, var_minutes)
    print """Stdev time to close req:        HOURS: {0}
                                  MIN: {1}""".format(sdev_hours, sdev_minutes)
    print "\nService distribution: Top 30 OPEN requests\n"
    # Remove the ".most_common(30)" function call to show all services
    pretty_print_dist(dict(service_distribution(req_open_fp).most_common(30)))
    print "\nService distribution: Top 30 CLOSED requests\n"
    pretty_print_dist(dict(service_distribution(req_closed_fp).most_common(30)))
    print "\nAgency distribution:  OPEN requests\n"
    pretty_print_dist(dict(agency_distribution(req_open_fp)))
    print "\nAgency distribution:  CLOSED requests\n"
    pretty_print_dist(dict(agency_distribution(req_closed_fp)))
