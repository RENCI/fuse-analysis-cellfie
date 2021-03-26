import requests


json_headers = {
    "Accept": "application/json"
}


json_post_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


config = {
    "title": "Aminoglycoside dosing guidance",
    "piid": "fuse-analysis-cellfie",
    "pluginType": "g",
    "settingsDefaults": {
        "pluginSelectors": [ {
            "title": "Drug",
            "id": "dosing.rxCUI",
            "selectorValue": {
                "value": "rxCUI:1596450",
                "title": "Gentamicin"
            }
        } ],
        "modelParameters": [ {
            "id": "fuse-analysis-cellfie:1",
            "title": "Extended interval nomogram",
            "parameterDescription": "This calculator uses one of four extended-interval nomograms. Please choose one nomogram.",
            "parameterValue": { "value": "Hartford" },
            "legalValues": {
                "type": "string",
                "enum": [ "Hartford", "Urban-Craig", "Conventional A", "Conventional B" ] }
        },
        {
            "id": "oid-6:dose",
            "title": "Dose",
            "parameterDescription": "Dose in mg unit for computing concentration graph",
            "parameterValue": {"value": 180},
            "legalValues": {"type": "number", "minimum": "120", "maximum": "240"}
        },
        {
            "id": "oid-6:tau",
            "title": "Frequency",
            "parameterDescription": "Dose frequency in hour unit for computing concentration graph",
            "parameterValue": {"value": 12},
            "legalValues": {"type": "number", "minimum": "8", "maximum": "16"}
        },
        {
            "id": "oid-6:num_cycles",
            "title": "Number of cycles",
            "parameterDescription": "Number of cycles in concentration graph",
            "parameterValue": {"value": 6},
            "legalValues": {"type": "number", "minimum": "4", "maximum": "8"}
        } ],
        "patientVariables": [ {
            "id": "LOINC:30525-0",
            "title": "Age",
            "legalValues": { "type": "number", "minimum": "0" },
            "why": "Age is used to calculate the creatinine clearance. Dosing is lower for geriatric patient and contraindicated for pediatric patients"
        }, {
            "id": "LOINC:29463-7",
            "title": "Weight",
            "legalValues": { "type": "number", "minimum": "0" },
            "why": "Weight is used to calculate the creatinine clearance. Dosing is higher for patients with higher weight"
        }, {
            "id": "LOINC:39156-5",
            "title": "BMI",
            "legalValues": { "type": "number", "minimum": "0" },
            "why": "BMI is used to calculate the creatinine clearance. Dosing is higher for patients with higher BMI"
        }]
    }
}

guidance_input = [{
    "piid": "fuse-analysis-cellfie",
    "patientId": "38",
    "settingsRequested": {
        "timestamp": "2019-12-03T13:41:09.942+00:00",
        "modelParameters": [ {
            "id": "fuse-analysis-cellfie:1",
            "title": "Extended interval nomogram",
            "parameterDescription": "This calculator uses one of four extended-interval nomograms. Please choose one nomogram.",
            "parameterValue": { "value": "Hartford" }
        } ],
        "patientVariables": [ {
            "id": "LOINC:30525-0",
            "title": "Age",
            "variableValue": {
                "value": "0.5",
                "units": "years"
            },
            "how": "The value was specified by the end user."
        }, {
            "id": "LOINC:39156-5",
            "title": "BMI",
            "variableValue": {
                "value": "0.5",
                "units": "kg/m^2"
            },
            "how": "The value was specified by the end user."
        } ]
    }
}]


php = "http://fuse-analysis-cellfie:8080"

def test_analysis():
    resp = requests.post(f"{php}/analysis", headers=json_post_headers, json=guidance_input)
    resp_output = resp.json()
    assert resp.status_code == 200
    assert len(resp_output) == 1
    assert "piid" in resp_output[0]
    assert "title" in resp_output[0]
    assert "advanced" in resp_output[0]
    assert "settingsUsed" in resp_output[0]
    assert "settingsRequested" in resp_output[0]
    assert "cards" in resp_output[0]
    for output in resp_output[0]['advanced']:
        assert "data" in output
        assert "specs" in output

def test_config():
    resp = requests.get(f"{php}/config", headers=json_headers)

    assert resp.status_code == 200
    assert resp.json() == config

    
def test_ui():
    resp = requests.get(f"{php}/ui")

    assert resp.status_code == 200
