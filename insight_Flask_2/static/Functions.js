document.addEventListener("DOMContentLoaded", function() {
    // Use serverOutput instead of hardcoded insights
    const insights = serverOutput;

    let currentActiveButton = null;

    // Function to display insight description in output container
    function displayInsightDescription(insight, index) {
        const outputContainer = document.getElementById("output");

        const insightDiv = document.createElement("div");
        insightDiv.classList.add("insight-item");

        const title = document.createElement("h3");
        title.textContent = insight.title;

        const description = document.createElement("p");
        description.textContent = insight.description;

        insightDiv.appendChild(title);
        insightDiv.appendChild(description);

        if (insight.requireChart === "true") {
            const visualizeBtn = document.createElement("button");
            visualizeBtn.textContent = "Visualize";
            visualizeBtn.classList.add("visualize-btn");
            visualizeBtn.addEventListener("click", function() {
                if (currentActiveButton) {
                    currentActiveButton.classList.remove("active");
                }
                visualizeBtn.classList.add("active");
                currentActiveButton = visualizeBtn;

                displayChart(insight.details);
            });
            insightDiv.appendChild(visualizeBtn);
        }

        outputContainer.appendChild(insightDiv);
    }

    // Function to display chart in graphContainer
    function displayChart(details) {
        Highcharts.chart('graphContainer', details);
    }

    // Display all insights
    Object.values(insights).forEach((insight, index) => {
        displayInsightDescription(insight, index);
    });

    // Display the first insight's chart by default if requireChart is true
    function displayFirstChart() {
        for (let insight of Object.values(insights)) {
            if (insight.requireChart === "true") {
                displayChart(insight.details);
                return;
            }
        }
    }

    displayFirstChart();
});