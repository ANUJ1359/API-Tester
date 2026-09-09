# AI-Assisted Automated REST API Testing System

## 📌 Project Overview

The AI-Assisted Automated REST API Testing System is a Python-based application developed to automate the testing and analysis of REST APIs.

The system sends requests to configured REST API endpoints, validates their responses, measures response time, detects incorrect or inconsistent behavior, identifies recurring failure patterns, and provides AI-assisted recommendations for the detected problems.

The project also provides an interactive web dashboard where developers can configure test cases, execute API tests, and view testing results, failure patterns, test history, and recommendations in one place.

This project was developed as a hackathon solution for automating REST API testing and improving API reliability.

---

# 🎯 Problem Statement

Testing REST APIs manually can be repetitive and time-consuming.

Developers need to verify several things when testing an API, such as:

- Whether the API is reachable
- Whether the correct HTTP status code is returned
- Whether the response contains the expected fields
- Whether the API responds within an acceptable time
- Whether repeated requests produce consistent results
- What type of problem is occurring when an API fails
- Whether the same problem is occurring repeatedly

The objective of this project is to automate these activities and provide a simple dashboard for analyzing the results.

---

# 💡 Proposed Solution

The system provides an automated REST API testing workflow.

The user can configure API test cases by specifying:

- Test case name
- API URL
- HTTP method
- Expected HTTP status code
- Expected response field
- Number of times the API should be tested

The testing engine executes these test cases and analyzes the responses.

The system then:

1. Sends requests to the API.
2. Checks the HTTP status code.
3. Validates the response structure.
4. Measures response time.
5. Repeats selected tests to detect inconsistent behavior.
6. Identifies the type of failure.
7. Analyzes recurring failure patterns.
8. Generates AI-assisted recommendations.
9. Displays the results through the dashboard.

---

# 🚀 Key Features

## 1. Automated REST API Testing

The system automatically sends HTTP requests to configured REST API endpoints.

Instead of manually testing each API, the tester executes all configured test cases automatically.

---

## 2. HTTP Status Code Validation

The system checks whether the API returns the expected HTTP status code.

For example:

```text
Expected Status: 200
Actual Status:   200
Result:          PASS
