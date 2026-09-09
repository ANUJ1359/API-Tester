from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import sys
import os
import json
import time
import random


app = FastAPI(title="REST API Automated Testing System")


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
# DEMO APIs
# ==========================================

@app.get("/")
def home():
    return {
        "message": "REST API Testing System is running"
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
            "message": "API working normally"
        }

    else:

        return {
            "error": "Something went wrong"
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

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    path = os.path.join(
        base_dir,
        "test_cases.json"
    )

    try:

        with open(path, "r") as file:
            return json.load(file)

    except:

        return []


# ==========================================
# ADD TEST CASE
# ==========================================

@app.post("/test-cases")
def add_test_case(test_case: TestCase):

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    path = os.path.join(
        base_dir,
        "test_cases.json"
    )

    try:

        with open(path, "r") as file:
            test_cases = json.load(file)

    except:

        test_cases = []


    new_test = test_case.model_dump()

    test_cases.append(new_test)


    with open(path, "w") as file:

        json.dump(
            test_cases,
            file,
            indent=4
        )


    return {
        "success": True,
        "message": "Test case added successfully",
        "test_case": new_test
    }


# ==========================================
# DELETE TEST CASE
# ==========================================

@app.delete("/test-cases/{index}")
def delete_test_case(index: int):

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    path = os.path.join(
        base_dir,
        "test_cases.json"
    )

    try:

        with open(path, "r") as file:
            test_cases = json.load(file)

    except:

        return {
            "success": False,
            "message": "Test cases file not found"
        }


    if index < 0 or index >= len(test_cases):

        return {
            "success": False,
            "message": "Invalid test case"
        }


    removed = test_cases.pop(index)


    with open(path, "w") as file:

        json.dump(
            test_cases,
            file,
            indent=4
        )


    return {
        "success": True,
        "message": "Test case deleted",
        "deleted": removed
    }


# ==========================================
# RUN TESTS
# ==========================================

@app.post("/run-tests")
def run_tests():

    try:

        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        tester_path = os.path.join(
            base_dir,
            "tester.py"
        )

        results_path = os.path.join(
            base_dir,
            "test_results.json"
        )

        history_path = os.path.join(
            base_dir,
            "test_history.json"
        )


        print("\n================================")
        print("RUNNING API TESTS")
        print("================================")


        result = subprocess.run(

            [sys.executable, tester_path],

            cwd=base_dir,

            capture_output=True,

            text=True,

            encoding="utf-8",

            errors="replace"
        )


        print(result.stdout)


        if result.stderr:

            print("ERROR:")
            print(result.stderr)


        # ------------------------------
        # RESULTS
        # ------------------------------

        if os.path.exists(results_path):

            with open(
                results_path,
                "r"
            ) as file:

                test_results = json.load(file)

        else:

            test_results = []


        # ------------------------------
        # HISTORY
        # ------------------------------

        if os.path.exists(history_path):

            with open(
                history_path,
                "r"
            ) as file:

                history = json.load(file)

        else:

            history = []


        return {

            "success":
                result.returncode == 0,

            "results":
                test_results,

            "history":
                history,

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

            "output": "",

            "error": str(e)
        }