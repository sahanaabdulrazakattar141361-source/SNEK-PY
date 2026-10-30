// ==========================================
// SNEK.PY MAIN JAVASCRIPT
// ==========================================


// ==========================================
// THEME SYSTEM
// ==========================================

const themeToggle = document.getElementById("themeToggle");


// Default theme = DARK
const savedTheme = localStorage.getItem("snekTheme");

if (savedTheme === "light") {
    document.body.classList.add("light");
} else {
    document.body.classList.remove("light");
}


// Theme button
if (themeToggle) {

    themeToggle.addEventListener("click", function () {

        document.body.classList.toggle("light");

        if (document.body.classList.contains("light")) {

            localStorage.setItem("snekTheme", "light");

        } else {

            localStorage.setItem("snekTheme", "dark");

        }

    });

}


// ==========================================
// CODE LAB
// ==========================================

const codeEditor = document.getElementById("codeEditor");
const runCodeButton = document.getElementById("runCodeButton");
const clearCodeButton = document.getElementById("clearCodeButton");
const codeOutput = document.getElementById("codeOutput");
const outputStatus = document.getElementById("outputStatus");


if (
    codeEditor &&
    runCodeButton &&
    clearCodeButton &&
    codeOutput
) {


    let pyodide = null;
    let loadingPromise = null;


    // ======================================
    // LOAD PYTHON ENGINE
    // ======================================

    async function loadPython() {

        // Already loaded
        if (pyodide) {
            return pyodide;
        }


        // Already loading
        if (loadingPromise) {
            return loadingPromise;
        }


        loadingPromise = (async function () {

            outputStatus.textContent = "Loading Python...";

            codeOutput.textContent =
                "🐍 Preparing the Python engine...\n\n" +
                "The first load may take a few seconds.";


            try {

                // Load Pyodide directly as a JavaScript module.
                const pyodideModule = await import(
                    "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.mjs"
                );


                pyodide = await pyodideModule.loadPyodide({
                    indexURL:
                        "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/"
                });


                outputStatus.textContent = "Python Ready ✓";

                codeOutput.textContent =
                    "🐍 Python is ready!\n\n" +
                    'Click "Run Code" to execute your program.';


                return pyodide;


            } catch (error) {

                console.error(
                    "Pyodide loading error:",
                    error
                );


                outputStatus.textContent = "Loading Error";


                codeOutput.textContent =
                    "❌ Could not load Python.\n\n" +
                    "Please make sure your internet connection is working.\n\n" +
                    "Then refresh the page and try again.";


                loadingPromise = null;

                throw error;

            }

        })();


        return loadingPromise;

    }


    // ======================================
    // RUN PYTHON
    // ======================================

    async function runPythonCode() {

        const code = codeEditor.value.trim();


        if (!code) {

            outputStatus.textContent = "Empty";

            codeOutput.textContent =
                "⚠️ Write some Python code first.";

            return;

        }


        runCodeButton.disabled = true;

        runCodeButton.textContent =
            "⏳ Running...";

        outputStatus.textContent =
            "Running...";

        codeOutput.textContent =
            "🐍 Running your Python code...";


        try {

            const python = await loadPython();


            let output = "";


            // Capture print() output
            python.setStdout({

                batched: function (text) {

                    output += text;

                }

            });


            // Capture errors
            python.setStderr({

                batched: function (text) {

                    output += text;

                }

            });


            await python.runPythonAsync(code);


            if (output.trim() === "") {

                output =
                    "✓ Code executed successfully.\n\n" +
                    "Your program did not produce any output.";

            }


            codeOutput.textContent =
                output;

            outputStatus.textContent =
                "Success ✓";


        } catch (error) {

            console.error(
                "Python execution error:",
                error
            );


            codeOutput.textContent =
                "❌ Python Error\n\n" +
                error.message;


            outputStatus.textContent =
                "Error";

        }


        runCodeButton.disabled = false;

        runCodeButton.textContent =
            "▶ Run Code";

    }


    // ======================================
    // RUN BUTTON
    // ======================================

    runCodeButton.addEventListener(
        "click",
        runPythonCode
    );


    // ======================================
    // CLEAR BUTTON
    // ======================================

    clearCodeButton.addEventListener(
        "click",
        function () {

            codeEditor.value = "";

            codeOutput.textContent =
                'Click "Run Code" to see your output...';

            outputStatus.textContent =
                "Ready";

            codeEditor.focus();

        }
    );


    // ======================================
    // QUICK EXAMPLES
    // ======================================

    const exampleCards =
        document.querySelectorAll(".example-card");


    exampleCards.forEach(function (card) {

        card.addEventListener(
            "click",
            function () {

                const code =
                    card.getAttribute("data-code");


                codeEditor.value =
                    code;


                codeOutput.textContent =
                    'Example loaded!\n\n' +
                    'Click "Run Code" ▶';


                outputStatus.textContent =
                    "Ready";


                codeEditor.focus();

            }
        );

    });


    // ======================================
    // TAB SUPPORT
    // ======================================

    codeEditor.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Tab") {

                event.preventDefault();


                const start =
                    codeEditor.selectionStart;

                const end =
                    codeEditor.selectionEnd;


                codeEditor.value =
                    codeEditor.value.substring(
                        0,
                        start
                    ) +
                    "    " +
                    codeEditor.value.substring(
                        end
                    );


                codeEditor.selectionStart =
                    codeEditor.selectionEnd =
                        start + 4;

            }

        }
    );

}