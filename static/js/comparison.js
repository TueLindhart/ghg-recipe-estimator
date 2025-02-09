document.addEventListener("DOMContentLoaded", function () {
  console.log("Comparison block JS loaded.");

  // Global function to fetch comparison data.
  window.fetchComparisonData = function (value, unit) {
    const apiUrl = `/api/comparison?value=${encodeURIComponent(
      value
    )}&unit=${encodeURIComponent(unit)}`;
    console.log("Fetching comparison data from:", apiUrl);
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error("API-svar ikke ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Comparison data received:", data);
        updateComparisonBlock(data);
      })
      .catch((err) => {
        console.error("Error fetching comparison data:", err);
      });
  };

  // Function to update the comparison block DOM with the API response.
  function updateComparisonBlock(data) {
    // Look for the container with the id "comparisonCards"
    const comparisonCards = document.getElementById("comparisonCards");
    if (!comparisonCards) {
      console.error("Comparison cards container not found");
      return;
    }
    // Update the inner HTML of the container with dynamic values.
    comparisonCards.innerHTML = `
      <div class="comparison-card">
        <p>${data.contextText}</p>
      </div>
    `;
  }
});
