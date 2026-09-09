import requests
import time
import json
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from ai_recommender import generate_recommendation


PERFORMANCE_LIMIT = 500

TEST_CASE_FILE = "test_cases.json"
RESULT_FILE = "test_results.json"
PATTERN_FILE = "failure_patterns.json"
HISTORY_FILE = "test_history.json"


with open(TEST_CASE_FILE, "r") as file:
    test_cases = json.load(file)


all_results = []
failure_patterns = {}


def add_failure_pattern(failure_type):

    if failure_type and failure_type != "NONE":

        failure_patterns[failure_type] = (
            failure_patterns.get(failure_type, 0) + 1
        )


def get_ai_recommendation(
    failure_type,
    response_time
):

    return generate_recommendation(
        failure_type,
        response_time
    )


print("\n==========================================")
print("        REST API AUTOMATED TESTER")
print("==========================================\n")


for test in test_cases:

    name = test["name"]
    url = test["url"]
    method = test["method"]
    expected_status = test["expected_status"]

    expected_field = test.get(
        "expected_field"
    )

    repeat = test.get(
        "repeat",
        1
    )


    # ======================================
    # REPEATED TEST
    # ======================================

    if repeat > 1:

        print(
            f"🔄 Testing {name} "
            f"({repeat} times)..."
        )

        responses = []


        for i in range(repeat):

            try:

                start = time.time()

                response = requests.request(
                    method,
                    url,
                    timeout=10
                )

                end = time.time()


                response_time = round(
                    (end - start) * 1000,
                    2
                )


                try:

                    data = response.json()

                except:

                    data = {}


                responses.append({

                    "status":
                        response.status_code,

                    "field_exists":
                        (
                            expected_field in data
                            if expected_field
                            else True
                        ),

                    "response_time":
                        response_time
                })


            except:

                responses.append({

                    "status": 0,

                    "field_exists": False,

                    "response_time": 0
                })


        statuses = [
            r["status"]
            for r in responses
        ]


        field_results = [
            r["field_exists"]
            for r in responses
        ]


        status_inconsistent = (
            len(set(statuses)) > 1
        )


        structure_inconsistent = (
            len(set(field_results)) > 1
        )


        avg_time = round(

            sum(
                r["response_time"]
                for r in responses
            )
            / len(responses),

            2
        )


        if (
            status_inconsistent
            or structure_inconsistent
        ):

            failure_type = (
                "INCONSISTENT RESPONSE"
            )

            result_status = "WARNING"

            add_failure_pattern(
                failure_type
            )


            ai = get_ai_recommendation(
                failure_type,
                avg_time
            )


            result = {

                "name": name,

                "method": method,

                "url": url,

                "status": statuses[-1],

                "response_time": avg_time,

                "result": result_status,

                "failure_type":
                    failure_type,

                "ai": ai
            }


            print(
                f"⚠️ {name} - "
                f"INCONSISTENT RESPONSE"
            )


        else:

            if (
                statuses[0]
                == expected_status
                and field_results[0]
            ):

                if avg_time > PERFORMANCE_LIMIT:

                    failure_type = (
                        "PERFORMANCE ISSUE"
                    )

                    result_status = "WARNING"

                    add_failure_pattern(
                        failure_type
                    )


                    ai = get_ai_recommendation(
                        failure_type,
                        avg_time
                    )


                    result = {

                        "name": name,

                        "method": method,

                        "url": url,

                        "status":
                            statuses[0],

                        "response_time":
                            avg_time,

                        "result":
                            result_status,

                        "failure_type":
                            failure_type,

                        "ai": ai
                    }


                    print(
                        f"⚠️ {name} - "
                        f"PERFORMANCE ISSUE"
                    )


                else:

                    result = {

                        "name": name,

                        "method": method,

                        "url": url,

                        "status":
                            statuses[0],

                        "response_time":
                            avg_time,

                        "result":
                            "PASS",

                        "failure_type":
                            "NONE",

                        "ai": None
                    }


                    print(
                        f"✅ {name}"
                    )


            else:

                failure_type = (
                    "RESPONSE VALIDATION ERROR"
                )

                result_status = "FAIL"

                add_failure_pattern(
                    failure_type
                )


                ai = get_ai_recommendation(
                    failure_type,
                    avg_time
                )


                result = {

                    "name": name,

                    "method": method,

                    "url": url,

                    "status":
                        statuses[0],

                    "response_time":
                        avg_time,

                    "result":
                        result_status,

                    "failure_type":
                        failure_type,

                    "ai": ai
                }


                print(
                    f"❌ {name} - "
                    f"RESPONSE VALIDATION ERROR"
                )


        all_results.append(result)

        continue


    # ======================================
    # NORMAL TEST
    # ======================================

    print(
        f"Testing {name}..."
    )


    try:

        start = time.time()


        response = requests.request(
            method,
            url,
            timeout=10
        )


        end = time.time()


        response_time = round(
            (end - start) * 1000,
            2
        )


        try:

            data = response.json()

        except:

            data = {}


        status_ok = (
            response.status_code
            == expected_status
        )


        structure_ok = True


        if expected_field:

            structure_ok = (
                expected_field in data
            )


        if not status_ok:

            failure_type = "STATUS ERROR"

            result_status = "FAIL"


        elif not structure_ok:

            failure_type = (
                "RESPONSE VALIDATION ERROR"
            )

            result_status = "FAIL"


        elif response_time > PERFORMANCE_LIMIT:

            failure_type = (
                "PERFORMANCE ISSUE"
            )

            result_status = "WARNING"


        else:

            failure_type = "NONE"

            result_status = "PASS"


        add_failure_pattern(
            failure_type
        )


        ai = None


        if failure_type != "NONE":

            ai = get_ai_recommendation(
                failure_type,
                response_time
            )


        result = {

            "name": name,

            "method": method,

            "url": url,

            "status":
                response.status_code,

            "response_time":
                response_time,

            "result":
                result_status,

            "failure_type":
                failure_type,

            "ai": ai
        }


        all_results.append(result)


        if result_status == "PASS":

            print(
                f"   ✅ PASS | "
                f"{response.status_code} | "
                f"{response_time} ms"
            )


        elif result_status == "WARNING":

            print(
                f"   ⚠️ WARNING | "
                f"{failure_type} | "
                f"{response_time} ms"
            )


        else:

            print(
                f"   ❌ FAIL | "
                f"{failure_type} | "
                f"{response.status_code}"
            )


    except Exception as e:

        failure_type = (
            "CONNECTION ERROR"
        )

        add_failure_pattern(
            failure_type
        )


        ai = get_ai_recommendation(
            failure_type,
            0
        )


        result = {

            "name": name,

            "method": method,

            "url": url,

            "status": 0,

            "response_time": 0,

            "result": "FAIL",

            "failure_type":
                failure_type,

            "ai": ai
        }


        all_results.append(result)


        print(
            f"   ❌ CONNECTION ERROR: "
            f"{str(e)}"
        )


# ==========================================
# SAVE RESULTS
# ==========================================

with open(
    RESULT_FILE,
    "w"
) as file:

    json.dump(
        all_results,
        file,
        indent=4
    )


# ==========================================
# SAVE FAILURE PATTERNS
# ==========================================

with open(
    PATTERN_FILE,
    "w"
) as file:

    json.dump(
        failure_patterns,
        file,
        indent=4
    )


# ==========================================
# SUMMARY
# ==========================================

total = len(all_results)

passed = sum(
    1 for r in all_results
    if r["result"] == "PASS"
)

failed = sum(
    1 for r in all_results
    if r["result"] == "FAIL"
)

warnings = sum(
    1 for r in all_results
    if r["result"] == "WARNING"
)


# ==========================================
# TEST HISTORY
# ==========================================

try:

    with open(
        HISTORY_FILE,
        "r"
    ) as file:

        history = json.load(file)

except:

    history = []


run_number = len(history) + 1


run_record = {

    "run":
        run_number,

    "timestamp":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

    "total":
        total,

    "passed":
        passed,

    "failed":
        failed,

    "warnings":
        warnings
}


history.append(
    run_record
)


history = history[-20:]


with open(
    HISTORY_FILE,
    "w"
) as file:

    json.dump(
        history,
        file,
        indent=4
    )


# ==========================================
# DISPLAY SUMMARY
# ==========================================

print("\n==========================================")
print("       📊 FAILURE PATTERN ANALYSIS")
print("==========================================")


if failure_patterns:

    for failure_type, count in \
        failure_patterns.items():

        print(
            f"{failure_type}: "
            f"{count} occurrence(s)"
        )


    most_common = max(
        failure_patterns,
        key=failure_patterns.get
    )


    print("\nMost Common Issue:")

    print(
        f"{most_common} → "
        f"{failure_patterns[most_common]} "
        f"occurrence(s)"
    )

else:

    print(
        "No failure patterns detected."
    )


print("\n==========================================")
print("             📈 TEST HISTORY")
print("==========================================")


print(
    f"Run #{run_number} → "
    f"PASS: {passed} | "
    f"FAIL: {failed} | "
    f"WARNING: {warnings}"
)


print("\n==========================================")
print("          TESTING COMPLETE")
print("==========================================\n")