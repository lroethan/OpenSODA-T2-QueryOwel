import requests
import argparse
import csv
import os
from datetime import datetime
from LRU_cache import LRUCache


BASE_URL = "https://oss.x-lab.info/open_digger/github/{}/{metric}.json"
DEFAULT_REPO = "X-lab2017/open-digger"
DEFAULT_METRIC = "openrank"

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


def fetch_json(repo, metric):
    url = BASE_URL.format(repo, metric=metric)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch JSON data.")
        return None


def write_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Metric', 'Month', 'Value'])
        for metric, month_data in data.items():
            for month, value in month_data.items():
                writer.writerow([metric, month, value])
            

def main():
    parser = argparse.ArgumentParser(description="OpenDigger Command Line Tool")
    parser.add_argument("--repo", default=DEFAULT_REPO, type=str, help="Repository name (e.g., X-lab2017/open-digger)")
    parser.add_argument("--metric", default=DEFAULT_METRIC, type=str, help="Metric name (e.g., OpenRank)")
    parser.add_argument("--month", type=str, help="Optional: Specify a month to get the specific value")
    args = parser.parse_args()

    repo = args.repo
    metric = args.metric.lower()

    result = {}
    cache = LRUCache(5)
    
    if metric == "all":
        for m in METRIC:
            json_data = cache.get((repo, m))
            if json_data is None:
                json_data = fetch_json(repo, m)
                if json_data:
                    cache.put((repo, m), json_data)
            if json_data:
                if args.month:
                    month_data = json_data.get(args.month)
                    if month_data:
                        print(f"{m} for {args.month}: {month_data}")
                        result[m] = {args.month: month_data}
                    else:
                        print(f"No data available for {args.month} in metric: {m}.")
                else:
                    print(json_data)
                    result[m] = json_data
    else:
        json_data = cache.get((repo, metric))
        if json_data is None:
            json_data = fetch_json(repo, metric)
            if json_data:
                cache.put((repo, metric), json_data)
        if json_data:
            if args.month:
                month_data = json_data.get(args.month)
                if month_data:
                    print(f"{metric} for {args.month}: {month_data}")
                    result[metric] = {args.month: month_data}
                else:
                    print(f"No data available for {args.month}.")
            else:
                print(json_data)
                result[metric] = json_data

    print(cache.cache_info())  
    os.makedirs("result", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"result/{timestamp}.csv"
    write_to_csv(filename, result)

if __name__ == "__main__":
    main()









