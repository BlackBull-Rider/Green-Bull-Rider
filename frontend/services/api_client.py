import requests

BASE_URL = "http://127.0.0.1:8000"


def get_dashboard():
    return requests.get(
        f"{BASE_URL}/dashboard"
    ).json()


def get_top_long_term():
    return requests.get(
        f"{BASE_URL}/dashboard/long-term"
    ).json()


def get_top_swing():
    return requests.get(
        f"{BASE_URL}/dashboard/swing"
    ).json()


def get_breakout():
    return requests.get(
        f"{BASE_URL}/dashboard/breakout"
    ).json()
