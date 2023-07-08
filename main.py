#!/usr/bin/env python
# coding=UTF-8

import requests
from argparse import ArgumentParser
import csv
import os
import sys
from datetime import datetime, timedelta
from collections import OrderedDict
import json


BASE_URL = "https://oss.x-lab.info/open_digger/github/{}/{metric}.json"
DEFAULT_REPO = "X-lab2017/open-digger"
DEFAULT_METRIC = "openrank"
DEFAULT_MONTH = "2022-06"

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
    "project_openrank_detail",
]

X_METRIC = [
    "openrank",
    "activity",
    "attention",
    "stars",
    "participants",
    "issue_comments",
    "activity_details",
    "developer_network",
    "repo_network",
    "project_openrank_detail",
]


C_METRIC = list(set(METRIC) - set(X_METRIC))


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def __repr__(self):
        return repr(self.cache)


class GlobalOptions(object):
    def __init__(self, options=None):
        self._options = options

    def __getitem__(self, name):
        return self._options.__dict__.get(name)

    def __getattr__(self, name):
        if name in dir(GlobalOptions) or name in self.__dict__:
            return getattr(self, name)
        elif name in self._options.__dict__:
            return getattr(self._options, name)
        else:
            raise AttributeError(
                "'%s' has no attribute '%s'" % (self.__class__.__name__, name)
            )


options = GlobalOptions()


class Colorizing(object):
    colors = {
        "none": "",
        "default": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "reverse": "\033[7m",
        "concealed": "\033[8m",
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "on_black": "\033[40m",
        "on_red": "\033[41m",
        "on_green": "\033[42m",
        "on_yellow": "\033[43m",
        "on_blue": "\033[44m",
        "on_magenta": "\033[45m",
        "on_cyan": "\033[46m",
        "on_white": "\033[47m",
        "beep": "\007",
    }

    @classmethod
    def colorize(cls, s, color=None):
        if options.color == "never":
            return s
        if options.color == "auto" and not sys.stdout.isatty():
            return s
        if color in cls.colors:
            return "{0}{1}{2}".format(cls.colors[color], s, cls.colors["default"])
        else:
            return s


def fetch_json(repo, metric):
    url = BASE_URL.format(repo, metric=metric)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def write_to_csv(filename, data):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Metric", "Month", "Value"])
        for metric, month_data in data.items():
            for month, value in month_data.items():
                writer.writerow([metric, month, value])


def parse_month(month):
    if "(" in month:
        # Discrete time points, e.g., (2022-02, 2022-05, 2021-09)
        return month.strip("()").split(", ")
    elif "[" in month:
        # Closed interval, e.g., [2022-02, 2022-06]
        start, end = month.strip("[]").split(", ")
        start_date = datetime.strptime(start, "%Y-%m")
        end_date = datetime.strptime(end, "%Y-%m")
        months = []
        while start_date <= end_date:
            months.append(start_date.strftime("%Y-%m"))
            start_date += timedelta(days=31)
        return months
    else:
        # Single time point, e.g., 2022-06
        return [month]


def parse_metric(metric):
    if "(" in metric:
        return metric.strip("()").split(", ")
    elif metric == "all":
        return METRIC
    elif metric == "x-all":
        return X_METRIC
    elif metric == "c-all":
        return C_METRIC
    else:
        return [metric]


def arg_parse():
    parser = ArgumentParser(description="OpenDigger Command Line Tool")

    parser.add_argument(
        "-r",
        "--repo",
        default=DEFAULT_REPO,
        type=str,
        help="Repository name (e.g., X-lab2017/open-digger) [GOLBAL SETTING] ",
    )
    parser.add_argument(
        "-m",
        "--metric",
        default=DEFAULT_METRIC,
        type=str,
        help="Metric name (e.g., OpenRank), or 'all' to get all metrics [GOLBAL SETTING]",
    )
    parser.add_argument(
        "-t",
        "--month",
        default=DEFAULT_MONTH,
        type=str,
        help="Optional: Specify a month to get the specific value [GOLBAL SETTING]",
    )
    parser.add_argument(
        "--color",
        choices=["always", "auto", "never"],
        default="auto",
        help="colorize the output. " "Default to 'auto' or can be 'never' or 'always'.",
    )

    return parser.parse_args()


def main():
    options._options = arg_parse()
    _c = Colorizing.colorize

    cache = LRUCache(5)

    try:
        import readline
    except ImportError:
        pass
    while True:
        try:
            repo_input = input("Repository Name: ")
            metric_input = input("Metric Name: ")
            month_input = input("Month: ")

            if repo_input != "":
                options.repo = repo_input

            if metric_input != "":
                options.metric = metric_input

            if month_input != "":
                options.month = month_input

        except KeyboardInterrupt:
            break
        except EOFError:
            break

        result = {}
        repo = options.repo
        l_metric = parse_metric(options.metric.lower())
        l_month = parse_month(options.month)

        print(_c(f"Repo.name = {repo}", "yellow"))
        header = "| {:<10} | {:<10} | {:<10} |".format("Metric", "Month", "Value")
        line = "+{:-^12}+{:-^12}+{:-^12}+".format("", "", "")

        print(line)
        print(header)
        print(line)

        for m in l_metric:
            json_data = cache.get((repo, m))
            if json_data is None:
                json_data = fetch_json(repo, m)
                if json_data:
                    cache.put((repo, m), json_data)
            if json_data:
                if l_month != ["-"]:
                    for month in l_month:
                        month_data = json_data.get(month)
                        if month_data:
                            output = "| {:<10} | {:<10} | {:<10} |".format(
                                m, month, month_data
                            )
                            print(output)
                            result[m] = {month: month_data}
                        else:
                            print(
                                "| {:<10} | {:<10} | {:<10} |".format(
                                    m, month, "No data"
                                )
                            )
                            print(line)
                else:
                    for month, month_data in json_data.items():
                        print(
                            "| {:<10} | {:<10} | {:<10} |".format(m, month, month_data)
                        )
                        print(line)
                        result[m] = {month: month_data}
        os.makedirs("result", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"result/{timestamp}.csv"
        write_to_csv(filename, result)
        
        is_continue = input("Continue? [Y/n] ")
        if is_continue.lower() == "n":
            break

    print("\nBye\U0001F989~")


if __name__ == "__main__":
    main()
