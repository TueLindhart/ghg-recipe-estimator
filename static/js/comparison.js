// static/js/comparison.js
document.addEventListener("DOMContentLoaded", function () {
    console.log("Comparison block JS loaded.");
  
    // Global function to fetch comparison data.
    window.fetchComparisonData = function(value, unit) {
      const apiUrl = `/api/comparison?value=${encodeURIComponent(value)}&unit=${encodeURIComponent(unit)}`;
      fetch(apiUrl)
        .then(response => {
          if (!response.ok) {
            throw new Error("API response not ok");
          }
          return response.json();
        })
        .then(data => {
          updateComparisonBlock(data);
        })
        .catch(err => {
          console.error("Error fetching comparison data:", err);
        });
    };
  
    // Function to update the comparison block DOM with the API response.
    function updateComparisonBlock(data) {
      // Assume the comparison block is rendered inside an element with class 'comparison'
      const comparisonBlock = document.querySelector('.comparison');
      if (!comparisonBlock) return;
  
      // Update the inner HTML with dynamic values
      comparisonBlock.innerHTML = `
        <h2>Comparison</h2>
        <div class="comparison-card">
          <p>${data.contextText}</p>
        </div>
      `;
    }
  });