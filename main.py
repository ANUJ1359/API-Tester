from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import sys
import os
import json
import time
import random


app = FastAPI(
    title="REST API Automated Testing System"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==========================================
# HELPER
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


def load_json_file(filename, default):
    path = os.path.join(
        BASE_DIR,
        filename
    )

    try:
        if os.path.exists(path):

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

    except Exception as e:

        print(
            f"Error reading {filename}: {e}"
        )

    return default


# ==========================================
# DEMO APIs
# ==========================================

@app.get("/")
def home():

    return {
        "message":
            "REST API Testing System is running"
    }


@app.get("/users")
def users():

    return {
        "users": [
            {
                "id": 1,
                "name": "Anuj"
            },
            {
                "id": 2,
                "name": "Rahul"
            }
        ]
    }


@app.get("/products")
def products():

    return {
        "products": [
            {
                "id": 1,
                "name": "Laptop",
                "price": 57500
            },
            {
                "id": 2,
                "name": "Phone",
                "price": 25000
            }
        ]
    }


@app.get("/orders")
def orders():

    return {
        "orders": [
            {
                "id": 101,
                "product": "Laptop",
                "status": "confirmed"
            }
        ]
    }


@app.get("/broken")
def broken():

    return {
        "error": "users field missing"
    }


@app.get("/slow")
def slow():

    time.sleep(3)

    return {
        "message": "Slow API response"
    }


@app.get("/unstable")
def unstable():

    if random.choice([True, False]):

        return {
            "message":
                "API working normally"
        }

    else:

        return {
            "error":
                "Something went wrong"
        }


# ==========================================
# TEST CASE MODEL
# ==========================================

class TestCase(BaseModel):

    name: str

    url: str

    method: str

    expected_status: int

    expected_field: str = ""

    repeat: int = 1


# ==========================================
# GET TEST CASES
# ==========================================

@app.get("/test-cases")
def get_test_cases():

    return load_json_file(
        "test_cases.json",
        []
    )


# ==========================================
# ADD TEST CASE
# ==========================================

@app.post("/test-cases")
def add_test_case(
    test_case: TestCase
):

    path = os.path.join(
        BASE_DIR,
        "test_cases.json"
    )

    test_cases = load_json_file(
        "test_cases.json",
        []
    )

    new_test = test_case.model_dump()

    test_cases.append(
        new_test
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            test_cases,
            file,
            indent=4
        )

    return {

        "success": True,

        "message":
            "Test case added successfully",

        "test_case":
            new_test

    }


# ==========================================
# DELETE TEST CASE
# ==========================================

@app.delete("/test-cases/{index}")
def delete_test_case(index: int):

    path = os.path.join(
        BASE_DIR,
        "test_cases.json"
    )

    test_cases = load_json_file(
        "test_cases.json",
        []
    )

    if (
        index < 0
        or index >= len(test_cases)
    ):

        return {

            "success": False,

            "message":
                "Invalid test case"

        }

    removed = test_cases.pop(
        index
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            test_cases,
            file,
            indent=4
        )

    return {

        "success": True,

        "message":
            "Test case deleted",

        "deleted":
            removed

    }


# ==========================================
# GET TEST RESULTS
# ==========================================

@app.get("/test-results")
def get_test_results():

    return load_json_file(
        "test_results.json",
        []
    )


# ==========================================
# GET FAILURE PATTERNS
# ==========================================

@app.get("/failure-patterns")
def get_failure_patterns():

    return load_json_file(
        "failure_patterns.json",
        {}
    )


# ==========================================
# GET TEST HISTORY
# ==========================================

@app.get("/test-history")
def get_test_history():

    return load_json_file(
        "test_history.json",
        []
    )


# ==========================================
# RUN TESTS
# ==========================================

@app.post("/run-tests")
def run_tests():

    try:

        tester_path = os.path.join(
            BASE_DIR,
            "tester.py"
        )

        print("\n================================")
        print("RUNNING API TESTS")
        print("================================")

        result = subprocess.run(

            [
                sys.executable,
                tester_path
            ],

            cwd=BASE_DIR,

            capture_output=True,

            text=True,

            encoding="utf-8",

            errors="replace"

        )

        print(
            result.stdout
        )

        if result.stderr:

            print("ERROR:")

            print(
                result.stderr
            )


        # ==================================
        # LOAD RESULTS
        # ==================================

        test_results = load_json_file(
            "test_results.json",
            []
        )


        # ==================================
        # LOAD HISTORY
        # ==================================

        history = load_json_file(
            "test_history.json",
            []
        )


        # ==================================
        # LOAD FAILURE PATTERNS
        # ==================================

        failure_patterns = load_json_file(
            "failure_patterns.json",
            {}
        )


        # ==================================
        # RETURN EVERYTHING
        # ==================================

        return {

            "success":
                result.returncode == 0,

            "results":
                test_results,

            "history":
                history,

            "failure_patterns":
                failure_patterns,

            "output":
                result.stdout,

            "error":
                result.stderr

        }


    except Exception as e:

        return {

            "success": False,

            "results": [],

            "history": [],

            "failure_patterns": {},

            "output": "",

            "error":
                str(e)

        }
