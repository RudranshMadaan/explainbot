
let selectedAudience = "eli5";

// Select difficulty level
const audienceButtons = document.querySelectorAll(".audience");

audienceButtons.forEach(button => {
    button.addEventListener("click", () => {

        audienceButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        selectedAudience = button.dataset.audience;
    });
});


// Generate explanation
const explainButton = document.getElementById("explainBtn");

explainButton.addEventListener("click", async () => {

    const term = document.getElementById("term").value.trim();
    const result = document.getElementById("result");
    const answer = document.getElementById("answer");
    const status = document.getElementById("status");

    if (!term) {
        status.textContent = "Please enter a technical term first.";
        result.classList.add("hidden");
        return;
    }

    explainButton.disabled = true;
    explainButton.textContent = "Thinking...";
    status.textContent = "Generating your explanation...";

    result.classList.add("hidden");

    try {

        const response = await fetch("/api/explain", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                term: term,
                audience: selectedAudience
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong.");
        }

        answer.textContent = data.answer;
        result.classList.remove("hidden");
        status.textContent = "";

        loadHistory();

    } catch (error) {

        status.textContent = error.message || "Unable to generate explanation. Please try again.";

    } finally {

        explainButton.disabled = false;
        explainButton.textContent = "Explain it to me →";

    }
});


// Load recent explanation history
async function loadHistory() {

    const historyContainer = document.getElementById("history");

    try {

        const response = await fetch("/api/history");

        if (!response.ok) {
            throw new Error("Unable to load history");
        }

        const history = await response.json();

        historyContainer.innerHTML = "";

        if (history.length === 0) {
            historyContainer.textContent = "No explanations yet. Try your first term!";
            return;
        }

        history.forEach(item => {

            const historyItem = document.createElement("div");
            historyItem.className = "history-item";

            const title = document.createElement("strong");
            title.textContent = item.term;

            const details = document.createElement("small");
            details.textContent = item.audience.toUpperCase();

            historyItem.appendChild(title);
            historyItem.appendChild(details);

            historyItem.addEventListener("click", () => {
                document.getElementById("term").value = item.term;
                document.getElementById("answer").textContent = item.answer;
                document.getElementById("result").classList.remove("hidden");
                document.getElementById("status").textContent = "";
            });

            historyContainer.appendChild(historyItem);

        });

    } catch (error) {
        historyContainer.textContent = "Could not load recent explanations.";
    }
}


// Load history when the page opens
loadHistory();
