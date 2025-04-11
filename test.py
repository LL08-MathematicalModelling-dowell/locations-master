import requests
import json
import time
import math


def dowell_time():
    url = "https://100009.pythonanywhere.com/dowellclock/"

    payload = json.dumps(
        {
            "timezone": "Asia/Singapore",
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)
    res = json.loads(response.text)
    print(res["dowelltime"])
    return res["dowelltime"]


def generate_process_queue(data):
    """
    {"success":true,"message":"Database 'process_queue_db' and collections created successfully.","database":{"name":"process_queue_db","id":"67cac9e93fb4f7ad9ac6c30e"},"collections":[{"name":"process_collection","id":"67cac9e93fb4f7ad9ac6c30f","fields":[]}]}
    [{"name":"process","id":"67e3b19881cf3a2257949f1f","fields":[]}]
    8755 --- {"success":true,"message":"Documents inserted successfully","inserted_ids":["67e3e538a9bc6987b55d93ab","67e3e538a9bc6987b55d93ac","67e3e538a9bc6987b55d93ad","67e3e538a9bc6987b55d93ae","67e3e538a9bc6987b55d93af"]}
    need to delete
    {"name":"process_v2","id":"67f39063926c83f301624f8f"
    8755
    """
    url = "https://datacube.uxlivinglab.online/api/crud/"

    data = []
    for h in range(0, 8770):
        hour_dict = {}
        hour_dict["hour"] = h
        for i in range(1, 3601):
            hour_dict[str(i)] = None
        data.append(hour_dict)
    #   print(data)

    for i in range(6650, 8770, 5):
        payload = json.dumps(
            {
                "database_id": "67cac9e93fb4f7ad9ac6c30e",
                "collection_name": "process_v2",
                "data": data[i : i + 5],
            }
        )

        # print(data[i:100])
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, headers=headers, data=payload)

        print(i, "---", response.text)


def fetch_data_from_master_db():

    payload = {}
    headers = {}

    current_dowell_clock_time = dowell_time()

    dowell_clock_time__x = current_dowell_clock_time - 6 * 24 * 60 * 60
    dowell_clock_time_y = current_dowell_clock_time - 5 * 24 * 60 * 60

    query_string = (
        "{"
        + '"home_appliance_stores.last_report_time.dowelltime":'
        + "{"
        + '"$gte":'
        + "{"
        + str(dowell_clock_time__x)
        + "},"
        + '"$lte":'
        + "{"
        + str(dowell_clock_time_y)
        + "}}"
        + ","
        + '"report_count":'
        + "{"
        + '"$gt": 1 }'
        "}"
    )

    query = {
        "$or": [
            {
                "home_appliance_stores": {
                    "$elemMatch": {
                        "last_report_time.dowelltime": {
                            "$gte": dowell_clock_time__x,
                            "$lte": dowell_clock_time_y,
                        },
                        "report_count": {"$gt": 1},
                    }
                }
            },
            # {
            #     "departmental_store": {
            #         "$elemMatch": {
            #             "dowell_time.dowelltime": {"$gte": 131800000, "$lte": 131900000}
            #         }
            #     }
            # },
        ]
    }

    query_string = json.dumps(query)

    print(query_string)

    url = f"https://datacube.uxlivinglab.online/api/crud?database_id=67c570a4eb35f83a656ee020&collection_name=singapore&filters={query_string}"
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)

    # print(result)
    return result["data"]


def fetch_hour_specific_document(hour):
    url = (
        'https://datacube.uxlivinglab.online/api/crud?database_id=67cac9e93fb4f7ad9ac6c30e&collection_name=process_v2&filter={"hour":"'
        + str(hour)
        + '"}'
    )

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)

    return result["data"][0]


def store_data_in_process_queue(data, trt, k):
    """
    {"success":true,"message":"Database 'process_queue_db' and collections created successfully.","database":{"name":"process_queue_db","id":"67cac9e93fb4f7ad9ac6c30e"},"collections":[{"name":"process_collection","id":"67cac9e93fb4f7ad9ac6c30f","fields":[]}]}
    [{"name":"process","id":"67e3b19881cf3a2257949f1f","fields":[]}]
    8755 --- {"success":true,"message":"Documents inserted successfully","inserted_ids":["67e3e538a9bc6987b55d93ab","67e3e538a9bc6987b55d93ac","67e3e538a9bc6987b55d93ad","67e3e538a9bc6987b55d93ae","67e3e538a9bc6987b55d93af"]}
    need to delete
    8755
    """
    url = "https://datacube.uxlivinglab.online/api/crud/"
    total_reporting_time = trt

    for i in range(k, len(data)):
        d = data[i]
        start_time = time.time()

        hour_value = math.floor(total_reporting_time / 3600)
        second_value = math.floor(total_reporting_time % 3600 + 1)
        print(
            "h--->", hour_value, "s--->", second_value, "tt--->", total_reporting_time
        )

        # The `schedule_time` variable in the `store_data_in_process_queue` function is being set
        # to a value that represents the scheduled time for a particular data entry to be
        # processed. This value is calculated based on the `total_reporting_time` and is used to
        # determine when the data should be processed or updated in the system.

        d["schedule_time"] = total_reporting_time + 24 * 3600
        ###
        ###
        ###
        ###
        ###
        ###
        ###
        ###

        hour_document = fetch_hour_specific_document(hour_value)

        hour_document[str(second_value)] = d
        # print(hour_document)
        doc_id = hour_document["_id"]

        del hour_document["_id"]
        del hour_document["is_deleted"]

        url = "https://datacube.uxlivinglab.online/api/crud/"
        payload = json.dumps(
            {
                "database_id": "67cac9e93fb4f7ad9ac6c30e",
                "collection_name": "process_v2",
                "filters": {"_id": doc_id},
                "update_data": hour_document,
            }
        )

        headers = {"Content-Type": "application/json"}
        response = requests.request("PUT", url, headers=headers, data=payload)

        end_time = time.time()
        current_report_insertion_time = end_time - start_time

        total_reporting_time = total_reporting_time + current_report_insertion_time

        print(
            start_time,
            " ",
            end_time,
            "cit--->",
            current_report_insertion_time,
            "tt-->",
            total_reporting_time,
            "i-->",
            i,
        )
        print(response.text)
    return total_reporting_time


# generate_process_queue({})
data = fetch_data_from_master_db()
print(len(data))
trt = 9748

for j in range(48, len(data)):
    d = data[j]
    for key in d:
        if key == "is_deleted" or key == "_id":
            continue

        print("j--->", j)
        # print(d[key])
        if isinstance(d[key], list):
            if j == 48:
                k = 303
            else:
                k = 1
            trt = store_data_in_process_queue(d[key], trt, k)

# print(data)
#
# store_data_in_process_queue(
#     [{"key1": "value1"}, {"key2": "value2"}, {"key3": "value3"}]
# )
#
# working_data = pop_out_data_from_process_queue()
#
# working_data_report = generate_report(working_data)
#
# save_report_in_db(working_data_report)
#


def load_data_in_process(index):
    pass


def generate_report(a_category_data):
    return "some report data"


def pop_out_data_from_process_queue():
    pass


def save_report_in_db(working_data_report):
    pass
