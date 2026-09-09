const API_BASE =
    "http://127.0.0.1:8000";


// ==========================================
// LOAD RESULTS
// ==========================================

async function loadResults() {

    try {

        const response = await fetch(
            "../test_results.json?t=" + Date.now()
        );

        const results =
            await response.json();


        displaySummary(results);

        displayResults(results);

        displayAIResults(results);

        await loadFailurePatterns();

        await loadHistory();

    }

    catch (error) {

        console.log(
            "No test results available yet."
        );

    }

}


// ==========================================
// SUMMARY
// ==========================================

function displaySummary(results) {

    const total = results.length;


    const passed =
        results.filter(
            r => r.result === "PASS"
        ).length;


    const failed =
        results.filter(
            r => r.result === "FAIL"
        ).length;


    const warnings =
        results.filter(
            r => r.result === "WARNING"
        ).length;


    document.getElementById(
        "totalApis"
    ).textContent = total;


    document.getElementById(
        "passedApis"
    ).textContent = passed;


    document.getElementById(
        "failedApis"
    ).textContent = failed;


    document.getElementById(
        "warningApis"
    ).textContent = warnings;

}


// ==========================================
// API RESULTS
// ==========================================

function displayResults(results) {

    const table =
        document.getElementById(
            "resultsTable"
        );


    if (!results.length) {

        table.innerHTML = `
            <tr>
                <td colspan="6">
                    No test results available
                </td>
            </tr>
        `;

        return;
    }


    table.innerHTML = "";


    results.forEach(result => {

        let statusClass;


        if (result.result === "PASS") {

            statusClass =
                "status-pass";

        }

        else if (result.result === "FAIL") {

            statusClass =
                "status-fail";

        }

        else {

            statusClass =
                "status-warning";

        }


        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>
                ${result.name}
            </td>

            <td>
                ${result.method}
            </td>

            <td>
                ${result.status}
            </td>

            <td>
                ${result.response_time} ms
            </td>

            <td class="${statusClass}">
                ${result.result}
            </td>

            <td>
                ${result.failure_type}
            </td>

        `;


        table.appendChild(row);

    });

}


// ==========================================
// AI RESULTS
// ==========================================

function displayAIResults(results) {

    const container =
        document.getElementById(
            "aiResults"
        );


    const failures =
        results.filter(
            r => r.ai
        );


    if (!failures.length) {

        container.innerHTML = `

            <div class="empty-state">

                <h3>
                    No Issues Detected
                </h3>

                <p>
                    All tested APIs are behaving normally.
                </p>

            </div>

        `;

        return;
    }


    container.innerHTML = "";


    failures.forEach(result => {

        const ai = result.ai;


        const card =
            document.createElement(
                "div"
            );


        card.className =
            "ai-card";


        card.innerHTML = `

            <h3>
                ${result.name}
            </h3>

            <p>
                <strong>Issue:</strong>
                ${result.failure_type}
            </p>

            <p>
                <strong>Diagnosis:</strong>
                ${ai.diagnosis}
            </p>

            <div class="ai-recommendation">

                <strong>
                    Recommendation:
                </strong>

                <p>
                    ${ai.recommendation}
                </p>

            </div>

        `;


        container.appendChild(card);

    });

}


// ==========================================
// FAILURE PATTERNS
// ==========================================

async function loadFailurePatterns() {

    try {

        const response = await fetch(
            "../failure_patterns.json?t="
            + Date.now()
        );


        const patterns =
            await response.json();


        displayFailurePatterns(
            patterns
        );

    }

    catch {

        console.log(
            "No failure patterns."
        );

    }

}


function displayFailurePatterns(patterns) {

    const container =
        document.getElementById(
            "failurePatterns"
        );


    const entries =
        Object.entries(patterns);


    if (!entries.length) {

        container.innerHTML = `

            <div class="empty-state">

                <h3>
                    No Failure Patterns Yet
                </h3>

                <p>
                    No recurring issues were detected.
                </p>

            </div>

        `;

        return;
    }


    entries.sort(
        (a, b) => b[1] - a[1]
    );


    let html = `
        <div class="pattern-grid">
    `;


    entries.forEach(
        ([type, count]) => {

            html += `

                <div class="pattern-card">

                    <div class="pattern-count">
                        ${count}
                    </div>

                    <div class="pattern-label">
                        ${type}
                    </div>

                </div>

            `;

        }
    );


    html += `</div>`;


    const mostCommon =
        entries[0];


    html += `

        <div class="most-common">

            <div class="most-common-title">
                MOST COMMON ISSUE
            </div>

            <div class="most-common-value">

                ${mostCommon[0]}
                →
                ${mostCommon[1]}
                occurrence(s)

            </div>

        </div>

    `;


    container.innerHTML = html;

}


// ==========================================
// HISTORY
// ==========================================

async function loadHistory() {

    try {

        const response = await fetch(
            "../test_history.json?t="
            + Date.now()
        );


        const history =
            await response.json();


        displayHistory(history);

    }

    catch {

        console.log(
            "No history available."
        );

    }

}


function displayHistory(history) {

    const table =
        document.getElementById(
            "historyTable"
        );


    if (!history ||
        !history.length) {

        table.innerHTML = `

            <tr>

                <td colspan="6">
                    No test history available
                </td>

            </tr>

        `;

        return;
    }


    table.innerHTML = "";


    [...history]
        .reverse()
        .forEach(run => {

            const row =
                document.createElement(
                    "tr"
                );


            row.innerHTML = `

                <td>
                    #${run.run}
                </td>

                <td>
                    ${run.timestamp}
                </td>

                <td>
                    ${run.total}
                </td>

                <td class="status-pass">
                    ${run.passed}
                </td>

                <td class="status-fail">
                    ${run.failed}
                </td>

                <td class="status-warning">
                    ${run.warnings}
                </td>

            `;


            table.appendChild(row);

        });

}


// ==========================================
// LOAD TEST CASES
// ==========================================

async function loadTestCases() {

    try {

        const response =
            await fetch(
                API_BASE + "/test-cases"
            );


        const testCases =
            await response.json();


        displayTestCases(
            testCases
        );

    }

    catch (error) {

        document.getElementById(
            "testCasesList"
        ).textContent =
            "Unable to load test cases.";

    }

}


// ==========================================
// DISPLAY TEST CASES
// ==========================================

function displayTestCases(testCases) {

    const container =
        document.getElementById(
            "testCasesList"
        );


    if (!testCases.length) {

        container.innerHTML = `

            <div class="empty-state">

                No test cases configured.

            </div>

        `;

        return;
    }


    container.innerHTML = "";


    testCases.forEach(
        (test, index) => {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "test-case-item";


            item.innerHTML = `

                <div class="test-case-info">

                    <div class="test-case-name">

                        ${test.name}

                    </div>

                    <div class="test-case-details">

                        ${test.method}
                        |
                        ${test.url}
                        |
                        Expected:
                        ${test.expected_status}
                        |
                        Field:
                        ${test.expected_field || "None"}
                        |
                        Repeat:
                        ${test.repeat}

                    </div>

                </div>


                <button
                    class="delete-button"
                    onclick="deleteTestCase(${index})">

                    Delete

                </button>

            `;


            container.appendChild(item);

        }
    );

}


// ==========================================
// ADD TEST CASE
// ==========================================

document
    .getElementById("addTestBtn")
    .addEventListener(
        "click",
        async function () {


            const name =
                document.getElementById(
                    "testName"
                ).value.trim();


            const url =
                document.getElementById(
                    "testUrl"
                ).value.trim();


            const method =
                document.getElementById(
                    "testMethod"
                ).value;


            const expectedStatus =
                Number(
                    document.getElementById(
                        "expectedStatus"
                    ).value
                );


            const expectedField =
                document.getElementById(
                    "expectedField"
                ).value.trim();


            const repeat =
                Number(
                    document.getElementById(
                        "repeatCount"
                    ).value
                );


            const message =
                document.getElementById(
                    "testCaseMessage"
                );


            if (!name || !url) {

                message.textContent =
                    "Please enter test name and API URL.";

                message.style.color =
                    "#ff6b6b";

                return;
            }


            try {

                const response =
                    await fetch(
                        API_BASE + "/test-cases",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({

                                    name: name,

                                    url: url,

                                    method: method,

                                    expected_status:
                                        expectedStatus,

                                    expected_field:
                                        expectedField,

                                    repeat:
                                        repeat

                                })
                        }
                    );


                const data =
                    await response.json();


                if (!data.success) {

                    throw new Error(
                        data.message
                    );

                }


                message.textContent =
                    "✓ Test case added successfully.";

                message.style.color =
                    "#4ade80";


                document.getElementById(
                    "testName"
                ).value = "";


                document.getElementById(
                    "testUrl"
                ).value = "";


                document.getElementById(
                    "expectedField"
                ).value = "";


                document.getElementById(
                    "repeatCount"
                ).value = 1;


                await loadTestCases();

            }

            catch (error) {

                message.textContent =
                    "Error: " +
                    error.message;

                message.style.color =
                    "#ff6b6b";

            }

        }
    );


// ==========================================
// DELETE TEST CASE
// ==========================================

async function deleteTestCase(index) {

    if (
        !confirm(
            "Delete this test case?"
        )
    ) {

        return;

    }


    try {

        const response =
            await fetch(
                API_BASE +
                "/test-cases/" +
                index,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                data.message
            );

        }


        await loadTestCases();

    }

    catch (error) {

        alert(
            "Unable to delete test case:\n"
            + error.message
        );

    }

}


// ==========================================
// RUN TESTS
// ==========================================

document
    .getElementById("runTestsBtn")
    .addEventListener(
        "click",
        async function () {

            const button =
                document.getElementById(
                    "runTestsBtn"
                );


            try {

                button.disabled = true;

                button.textContent =
                    "⏳ Running...";


                const response =
                    await fetch(
                        API_BASE +
                        "/run-tests",
                        {
                            method: "POST"
                        }
                    );


                const data =
                    await response.json();


                if (!data.success) {

                    throw new Error(
                        data.error ||
                        "Tester execution failed"
                    );

                }


                displaySummary(
                    data.results
                );


                displayResults(
                    data.results
                );


                displayAIResults(
                    data.results
                );


                await loadFailurePatterns();


                if (data.history) {

                    displayHistory(
                        data.history
                    );

                }


                document.getElementById(
                    "lastRun"
                ).textContent =
                    "Tests completed successfully";


            }

            catch (error) {

                console.error(error);


                document.getElementById(
                    "lastRun"
                ).textContent =
                    "Test execution failed";


                alert(
                    "Error running tests:\n"
                    + error.message
                );

            }


            finally {

                button.disabled = false;

                button.textContent =
                    "▶ Run Tests";

            }

        }
    );


// ==========================================
// INITIAL LOAD
// ==========================================

loadResults();

loadTestCases();