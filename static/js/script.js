let currentInputURL = ""; // To store the user-entered URL
let currentChart = null; // To store the current chart instance

document.addEventListener("DOMContentLoaded", () => {
  const calculateButton = document.getElementById("calculateButton");
  const urlInput = document.getElementById("urlInput");
  const statusDiv = document.getElementById("statusDiv");

  calculateButton.addEventListener("click", async () => {
    const input_data = urlInput.value.trim();
    if (!input_data) {
      statusDiv.textContent = "Angiv venligst en URL.";
      return;
    }

    currentInputURL = input_data; // Store the URL user provided

    statusDiv.textContent =
      "Beregner CO2-udledning (dette kan tage et minut eller to)...";

    try {
      const startResponse = await fetch(
        `/calculate?input_data=${encodeURIComponent(input_data)}`
      );
      if (startResponse.status !== 202) {
        statusDiv.textContent = "Fejl ved start af estimering.";
        return;
      }

      const startData = await startResponse.json();
      const inputHash = startData.hashed_input;
      pollForResult(inputHash);
    } catch (error) {
      statusDiv.textContent = `Der opstod en fejl: ${error.message}`;
    }
  });
});

async function pollForResult(inputHash) {
  const statusDiv = document.getElementById("statusDiv");
  try {
    const response = await fetch(`/results/${inputHash}`);
    const data = await response.json();

    if (data.status === "Processing") {
      statusDiv.textContent = "Arbejder stadig på det ... vent venligst.";
      setTimeout(() => pollForResult(inputHash), 2000);
    } else if (data.status === "Completed") {
      const parsedData = JSON.parse(data.result);
      updateUI(parsedData);
      // Clear the status message
      statusDiv.textContent = "";
    } else {
      statusDiv.textContent = "Uventet svarstatus.";
    }
  } catch (error) {
    statusDiv.textContent = `Der opstod en fejl: ${error.message}`;
  }
}

function updateUI(parsedData) {
  // Update summary
  document.getElementById("totalCO2").textContent =
    parsedData.total_co2_kg || "-";
  document.getElementById("numberOfPersons").textContent =
    parsedData.number_of_persons || "-";
  document.getElementById("co2PerPerson").textContent =
    parsedData.co2_per_person_kg || "-";

  const avgRange = parsedData.avg_meal_emission_per_person_range_kg;
  if (avgRange && avgRange.length === 2) {
    document.getElementById(
      "avgRange"
    ).textContent = `${avgRange[0]} - ${avgRange[1]}`;
  } else {
    document.getElementById("avgRange").textContent = "";
  }

  // Update ingredients.
  const cardsContainer = document.getElementById("ingredientCards");
  cardsContainer.innerHTML = "";
  parsedData.ingredients.forEach((ing) => {
    const card = document.createElement("div");
    card.className = "ingredient-card";

    const title = document.createElement("h3");
    title.textContent = ing.name;

    const weight = document.createElement("p");
    weight.textContent = `Vægt: ${
      ing.weight_kg !== null ? ing.weight_kg + " kg" : "-"
    }`;

    const co2perkg = document.createElement("p");
    co2perkg.textContent = `Udledning pr. kg: ${
      ing.co2_per_kg !== null ? ing.co2_per_kg + " kg CO2e / kg" : "-"
    }`;

    const co2 = document.createElement("h4");
    co2.textContent = `Udledning: ${
      ing.co2_kg !== null ? ing.co2_kg + " kg" : "-"
    }`;

    const commentButton = document.createElement("button");
    commentButton.textContent = "Vis Noter";
    commentButton.style.cursor = "pointer";
    commentButton.style.position = "relative";
    commentButton.addEventListener("click", (event) => {
      showTooltip(
        event.target,
        `Beregning Noter: ${
          ing.calculation_notes !== null
            ? ing.calculation_notes
            : "Ingen noter tilgængelige"
        }
Vægt Estimering Noter: ${
          ing.weight_estimation_notes !== null
            ? ing.weight_estimation_notes
            : "Ingen noter tilgængelige"
        }
CO2e Udledning Noter: ${
          ing.co2_emission_notes !== null
            ? ing.co2_emission_notes
            : "Ingen noter tilgængelige"
        }`
      );
    });

    card.appendChild(title);
    card.appendChild(weight);
    card.appendChild(co2perkg);
    card.appendChild(co2);
    card.appendChild(commentButton);
    cardsContainer.appendChild(card);
  });

  // Initialize the bar chart with the ingredients data
  initializeBarChart(parsedData.ingredients);

  // **Call the comparison API**:
  // Check that the total emission is available before calling.
  if (window.fetchComparisonData && parsedData.total_co2_kg) {
    console.log(
      "Kalder fetchComparisonData med total_co2_kg:",
      parsedData.total_co2_kg
    );
    window.fetchComparisonData(parsedData.total_co2_kg, "kg");
  }
}
// Function to show a tooltip near the button
function showTooltip(button, text) {
  // Remove any existing tooltip
  let existingTooltip = document.querySelector(".tooltip-box");
  if (existingTooltip) {
    existingTooltip.remove();
  }

  // Create tooltip
  const tooltip = document.createElement("div");
  tooltip.className = "tooltip-box";

  // Use <pre> to preserve line breaks
  const pre = document.createElement("pre");
  pre.textContent = text;
  tooltip.appendChild(pre);

  // Position the tooltip near the button
  tooltip.style.position = "absolute";
  tooltip.style.background = "black";
  tooltip.style.color = "white";
  tooltip.style.padding = "5px 10px";
  tooltip.style.borderRadius = "5px";
  tooltip.style.fontSize = "12px";
  tooltip.style.whiteSpace = "pre-wrap"; // Preserve line breaks and wrap text
  tooltip.style.boxShadow = "0px 2px 5px rgba(0, 0, 0, 0.3)";
  tooltip.style.maxWidth = "600px"; // Double the width of the tooltip
  tooltip.style.overflowX = "auto"; // Enable horizontal scroll
  tooltip.style.width = "auto"; // Allow the width to adjust based on content
  tooltip.style.height = "auto"; // Allow the height to adjust based on content

  document.body.appendChild(tooltip);

  // Get button position
  const rect = button.getBoundingClientRect();
  tooltip.style.left = `${rect.left + window.scrollX}px`;
  tooltip.style.top = `${
    rect.top + window.scrollY - tooltip.offsetHeight - 10
  }px`; // Position above button

  // Remove tooltip on click outside
  setTimeout(() => {
    document.addEventListener("click", function removeTooltip(event) {
      if (!tooltip.contains(event.target) && event.target !== button) {
        tooltip.remove();
        document.removeEventListener("click", removeTooltip);
      }
    });
  }, 10);
}

function initializeBarChart(ingredientData) {
  const filteredData = ingredientData.filter(
    (ingredient) => ingredient.co2_kg !== null && ingredient.co2_kg > 0
  );

  const ctx = document.getElementById("emissionsChart").getContext("2d");

  // Destroy the existing chart if it exists
  if (currentChart) {
    currentChart.destroy();
  }

  currentChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: filteredData.map((ingredient) => ingredient.name),
      datasets: [
        {
          label: "CO2e udledninger (kg)",
          data: filteredData.map((ingredient) => ingredient.co2_kg),
          backgroundColor: "rgb(12, 61, 61)",
          borderColor: "rgb(6, 31, 31)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      indexAxis: "y", // This makes the bar chart horizontal
      maintainAspectRatio: false,
      responsive: true,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        x: {
          beginAtZero: true,
          title: {
            display: true,
            text: "CO2 udledning (kg)",
          },
        },
      },
    },
  });
}
