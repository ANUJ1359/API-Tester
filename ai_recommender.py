def generate_recommendation(
    failure_type,
    response_time=0
):

    if failure_type == "PERFORMANCE ISSUE":

        return {
            "diagnosis":
                f"API response time is high "
                f"({response_time} ms).",

            "recommendation":
                "Check database queries, "
                "external API calls, server "
                "processing time and caching."
        }


    if failure_type == "RESPONSE VALIDATION ERROR":

        return {
            "diagnosis":
                "The API response does not "
                "match the expected structure.",

            "recommendation":
                "Verify the response schema "
                "and ensure all required fields "
                "are returned."
        }


    if failure_type == "STATUS ERROR":

        return {
            "diagnosis":
                "The API returned an unexpected "
                "HTTP status code.",

            "recommendation":
                "Check server-side validation, "
                "routing and HTTP status handling."
        }


    if failure_type == "INCONSISTENT RESPONSE":

        return {
            "diagnosis":
                "Repeated requests produced "
                "different response structures "
                "or status codes.",

            "recommendation":
                "Investigate conditional logic, "
                "unstable dependencies and "
                "error-handling mechanisms."
        }


    if failure_type == "CONNECTION ERROR":

        return {
            "diagnosis":
                "The API could not be reached.",

            "recommendation":
                "Check whether the server is running, "
                "verify the API URL and inspect "
                "network connectivity."
        }


    return {
        "diagnosis":
            "No issue detected.",

        "recommendation":
            "No action required."
    }