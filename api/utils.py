import os
import requests
from random import seed, random


def _get_random(min_num, max_num):
    return random() * (max_num - min_num) + min_num


def generate_time_series_data(n):
    data = []
    seed()
    for i in range(n):
        if i == 0:
            y = _get_random(0, 1)
        else:
            y = max(data[i-1]['y'] + _get_random(-1, 1), 0)
        data.append({
            'x': i,
            'y': y
        })

    return data


def generate_multi_time_series_data(n, m):
    data = []
    seed()
    for i in range(m):
        group = 'group {}'.format(i)
        for j in range(n):
            if j == 0:
                y = _get_random(0, 1)
            else:
                y = max(data[len(data) - 1]['y'] + _get_random(-1, 1), 0)
            data.append({
                'x': j,
                'y': y,
                'group': group
            })
    return data


def generate_scatter_plot_data(n):
    data = []
    seed()
    a = _get_random(-1, 1)
    b = _get_random(0, 1)

    for i in range(n):
        x = _get_random(-1, 1)
        y = x * a + _get_random(0, b)
        data.append({'x': x, 'y': y})

    return data


def generate_multi_scatter_plot_data(n, m):
    data = []
    seed()
    for i in range(m):
        group = 'group {}'.format(i)
        a = _get_random(-1, 1)
        b = _get_random(0, 1)
        for j in range(n):
            x = _get_random(-1, 1)
            y = x * a + _get_random(0, b)
            data.append({
                'x': x,
                'y': y,
                'group': group
            })
    return data


def generate_histogram_data(n):
    data = []
    seed()
    for i in range(n):
        x = round(_get_random(1, 10))
        data.append({
            'x': x
        })
    return data


def generate_dosing_inputs(dose=None, tau=None, num_cycles=None):
    if not dose:
        dose = _get_random(120, 240)
    if not tau:
        tau = int(_get_random(8, 16))
    if not num_cycles:
        num_cycles = int(_get_random(4, 8))
    ret_input = [{
        "id": "dose",
        "title": "dose",
        "parameterDescription": "dose in mg unit for computing concentration graph",
        "parameterValue": {"value": dose},
        "legalValues": {"type": "number", "minimum": "120", "maximum": "240"}
    },
        {
            "id": "tau",
            "title": "frequency",
            "parameterDescription": "dose frequency in hour unit for computing concentration graph",
            "parameterValue": {"value": tau},
            "legalValues": {"type": "number", "minimum": "8", "maximum": "16"}
        },
        {
            "id": "num_cycles",
            "title": "Number of cycles",
            "parameterDescription": "number of cycles in concentration graph",
            "parameterValue": {"value": num_cycles},
            "legalValues": {"type": "number", "minimum": "4", "maximum": "8"}
        }]
    return dose, tau, num_cycles, ret_input


def generate_dosing_data(p_age=None, p_weight=None, p_bmi=None, dose=None, tau=None, num_cycles=None):
    fuse_host = os.getenv("FUSE_HOST", "localhost")
    fuse_port = os.getenv("FUSE_PORT", "8080")
    fuse_version = os.getenv("FUSE_VERSION", "v1")
    json_post_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    if p_weight:
        vd = 0.3 * float(p_weight)
    elif p_bmi:
        weight = float(p_bmi) * 1.7 ** 2
        vd = 0.3 * weight
    else:
        vd = _get_random(22, 25)

    if p_weight and p_age:
        crcl = ((140 - float(p_age)) * float(p_weight))/(72 * 1.56)
    elif p_bmi and p_age:
        weight = float(p_bmi) * 1.7 ** 2
        crcl = ((140 - float(p_age)) * weight) / (72 * 1.56)
    else:
        crcl = _get_random(29.3516, 63.4812)
    seed()
    input_dose, input_tau, input_num_cycles, _ = generate_dosing_inputs(dose=dose, tau=tau, num_cycles=num_cycles)
    post_input = {
        "dose": input_dose,
        "tau": input_tau,
        "crcl":  crcl,
        "t_infusion": 0.5,
        "vd": vd,
        "num_cycles": input_num_cycles
    }

    url_str = "http://{}:{}/{}/plugin/tx-generator-dosing/concentration_data".format(fuse_host, fuse_port, fuse_version)
    resp = requests.post(url_str, headers=json_post_headers, json=post_input)
    if resp.status_code == 200:
        return resp.json()
    else:
        return []


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    src = os.path.join("/usr/src/app/data/", filename)
    return open(src).read()
