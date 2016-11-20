import re
import json
import time
import math
import calendar
import operator
from collections import Counter

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

def service_distribution(requests):
    cnt = Counter()
    for req in requests:
        cnt[req['service_code']] += 1

    return cnt


def agency_distribution(requests):
    cnt = Counter()
    for req in requests:
        cnt[req['agency_responsible']] += 1

    return cnt


def num_requests(requests):
    cnt = service_distribution(requests)
    return sum(cnt.values())


def close_time_to_arr(requests):
    completion_time_arr = []
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

        # Someone goof'd when inputting times, ensure difference is positive
        completion_time_arr.append(abs(end_time - start_time))

    return completion_time_arr, no_update_time, no_expected_time

def close_times_by_agency_dict(requests):
    agencies = {"agencies":{}}
    for req in requests:
        agency = "none" if req["agency_responsible"] == '' else req["agency_responsible"]
        if not agencies["agencies"].has_key(agency):
            agencies["agencies"][agency] = [req]
        else:
            agencies["agencies"][agency].append(req)
    return agencies

def variance_close_times(times_arr, avg_of_arr):
    return sum(map(lambda x: (x - avg_of_arr)**2, times_arr)) / len(times_arr)

def pretty_print_dist(dist_dict):
    max_spaces = len(max(dist_dict.keys(), key=len)) + 3
    max_value  = max(dist_dict.values())
    sum_values = sum(dist_dict.values())
    sorted_dist_dict = sorted(dist_dict.items(), key=operator.itemgetter(1), reverse=True)
    for tup in sorted_dist_dict:
        num_spaces      = max_spaces - len(tup[0])
        num_bars        = int((tup[1] / float(max_value)) * 50) + 1
        pcnt_of_total   = " ("+str(round(tup[1] / float(sum_values),3))+")"
        print str(tup[0])+":"+(" "*num_spaces)+("|"*num_bars)+"  "+str(tup[1])+pcnt_of_total


if __name__ == "__main__":

    req_open_fp = "./data/requests_20160101_20161119_OPEN.json"
    req_closed_fp = "./data/requests_20160101_20161119_CLOSED.json"
    with open(req_open_fp, 'r+') as fo:
        open_requests = json.load(fo)
    with open(req_closed_fp, 'r+') as fc:
        closed_requests = json.load(fc)

    all_closed      = num_requests(closed_requests)
    all_open        = num_requests(open_requests)
    compl_time_arr, no_close, no_expected = close_time_to_arr(closed_requests)
    num_zeros        = Counter(compl_time_arr)[0]
    filtered_compl_time_arr  = filter(lambda x: x > 0, compl_time_arr)

    # Average close times for all agencies
    total_avg_close_times = close_times_by_agency_dict(closed_requests)
    agency_close_times = []
    for key in total_avg_close_times["agencies"].keys():
        close_times = close_time_to_arr(total_avg_close_times["agencies"][key])[0]
        num_req = len(close_times)
        agency_avg_close_time = sum(close_times)/num_req if num_req != 0 else 0
        agency_close_times.append(dict(agency=key,
                                       num_req=len(close_times),
                                       avg_close_t=agency_avg_close_time))
    sum_of_avg = 0
    agency_avg_strings = ""
    for obj in sorted(agency_close_times, key=lambda k: k["avg_close_t"], reverse=True):
        sum_of_avg += obj["avg_close_t"]
        agency_avg_strings += "Agency: {0}, num req: {1}, avg close time: {2}\n".format(obj["agency"], obj["num_req"], obj["avg_close_t"]/3600)

    total_avg_all_agency = sum_of_avg/len(filter(lambda x: x["avg_close_t"] > 0, agency_close_times))
    var_comp_time   = variance_close_times(filtered_compl_time_arr, total_avg_all_agency)
    var_hours       = int(var_comp_time)/3600
    var_minutes     = (int(var_comp_time)%3600)/60
    sdev_hours      = int(math.sqrt(var_comp_time))/3600
    sdev_minutes    = (int(math.sqrt(var_comp_time))%3600)/60

    print "\n======================================================="
    print "                     REQUESTS REPORT                     "
    print "=======================================================\n"
    print "Num total req:                         {0} (%100)".format(all_closed+all_open)
    print "Req closed with no close time:         {0} (%{1})".format(no_close, round(no_close/float(all_closed),2))
    print "Req closed with no expected close time:{0} (%{1})".format(no_expected, round(no_expected/float(all_closed),2))
    print "Num requests serviced in 0 time:       {0} (%{1})\n".format(num_zeros, round(num_zeros/float(all_closed),2))
    print """Extremes (hours):                 MIN: {0}
                                  MAX: {1}""".format(min(compl_time_arr)/3600, max(compl_time_arr)/3600)
    print """Average across all agencies:    HOURS: {0}
                                  MIN: {1}""".format(total_avg_all_agency/3600, (total_avg_all_agency%3600)/60)
    print """Var time to close req:          HOURS: {0}
                                  MIN: {1}""".format(var_hours, var_minutes)
    print """Stdev time to close req:        HOURS: {0}
                                  MIN: {1}\n""".format(sdev_hours, sdev_minutes)
    print "Avg close times by agency:\n"
    print agency_avg_strings
    # Remove the ".most_common(30)" function call to show all services
    print "\nService distribution: 2016 Top 30 OPEN requests\n"
    pretty_print_dist(dict(service_distribution(open_requests).most_common(30)))
    print "\nService distribution: 2016 Top 30 CLOSED requests\n"
    pretty_print_dist(dict(service_distribution(closed_requests).most_common(30)))
    print "\nAgency distribution: 2016 OPEN requests\n"
    pretty_print_dist(dict(agency_distribution(open_requests)))
    print "\nAgency distribution: 2016 CLOSED requests\n"
    pretty_print_dist(dict(agency_distribution(closed_requests)))

    def print_year_dist(requests, year):
        print "\nService distribution: Year {}\n".format(year)
        pretty_print_dist(dict(service_distribution(requests).most_common(30)))
        print "\nAgency distribution:  Year {}\n".format(year)
        pretty_print_dist(dict(agency_distribution(requests)))
        print "Total num reqs:      {}".format(len(requests))

    for i in reversed(range(6)):
        year = '201{}'.format(i)
        fname = './data/requests_'+year+'0101_'+year+'1231_CLOSED.json'
        with open(fname,'r') as f:
            reqs = json.load(f)
        print_year_dist(reqs,year)
