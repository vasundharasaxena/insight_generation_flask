document.addEventListener("DOMContentLoaded", function() {
    if (serverOutput) {
        console.log("Server Output:", serverOutput); // Debug log

        document.getElementById("output").innerHTML = "<h3>Insights:</h3>";
        const insights = serverOutput;

        let currentActiveButton = null;

        // Function to display insight description in output container
        function displayInsightDescription(insight, index) {
            console.log(`Insight ${index}:`, insight); // Debug log

            const outputContainer = document.getElementById("output");

            const insightDiv = document.createElement("div");
            insightDiv.classList.add("insight-item");

            const newline = document.createElement("br");
            insightDiv.appendChild(newline);

            const title = document.createElement("h3");
            title.textContent = insight.title;

            const description = document.createElement("p");
            description.textContent = insight.description;

            insightDiv.appendChild(title);
            insightDiv.appendChild(description);

            // More flexible check for requireChart
            if (insight.requireChart === true || insight.requireChart === "true") {
                console.log(`Creating Visualize button for insight ${index}`); // Debug log

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

                const newline = document.createElement("br");
                
                insightDiv.appendChild(visualizeBtn);
                insightDiv.appendChild(newline);
            } else {
                console.log(`No Visualize button for insight ${index}, requireChart:`, insight.requireChart); // Debug log
            }

            outputContainer.appendChild(insightDiv);
        }

        // Function to display chart in graphContainer
        function displayChart(details) {
            console.log("Displaying chart with details:", details); // Debug log
            Highcharts.chart('graphContainer', details);
        }

        // Display all insights
        Object.values(insights).forEach((insight, index) => {
            displayInsightDescription(insight, index);
        });

        // Display the first insight's chart by default if requireChart is true
        function displayFirstChart() {
            for (let insight of Object.values(insights)) {
                if (insight.requireChart === true || insight.requireChart === "true") {
                    displayChart(insight.details);
                    return;
                }
            }
        }

        displayFirstChart();

        // Apply scrollable style to output container
        const outputContainer = document.getElementById("output");
        outputContainer.style.overflowY = 'auto'; // Enable vertical scrolling
    } else {
        console.log("No server output available"); // Debug log
    }
});