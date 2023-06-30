import requests


DEFAULT_TARGET = "X-lab2017/open-digger"

METRIC = [
    "openrank",
    "activity",
    "attention",
    "active_dates_and_times",
    "stars",
    "technical_fork",
    "participants",
    "new_contributors",
    "new_contributors_detail",
    "inactive_contributors",
    "bus_factor",
    "bus_factor_detail",
    "issues_new",
    "issues_closed",
    "issue_comments",
    "issue_response_time",
    "issue_resolution_duration",
    "issue_age",
    "code_change_lines_add",
    "code_change_lines_remove",
    "code_change_lines_sum",
    "change_requests",
    "change_requests_accepted",
    "change_requests_reviews",
    "change_request_response_time",
    "change_request_resolution_duration",
    "change_request_age",
    "activity_details",
    "developer_network",
    "repo_network",
    "project_openrank_detail"
]


def fetch_json(target, metric):
    url = f"https://oss.x-lab.info/open_digger/github/{target}/{metric}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_value_by_month(data, month):
    if month in data:
        return data[month]
    else:
        return None

if __name__ == '__main__':
    target = DEFAULT_TARGET
    metric = "project_openrank_detail"
    json_data = fetch_json(target, metric)
    if json_data is not None:
        print("JSON data fetched successfully.")
        month = input("Enter the month (optional): ")
        if month:
            value = get_value_by_month(json_data, month)
            if value is not None:
                print(f"Value for {metric} in {month}: {value}")
            else:
                print(f"No data available for {metric} in {month}.")
        else:
            print("No specific month provided.")
    else:
        print("Failed to fetch JSON data.")




