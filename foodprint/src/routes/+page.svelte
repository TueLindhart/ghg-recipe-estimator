<script>
  import { onMount } from 'svelte';

  // If your FastAPI runs on http://localhost:8000, store that base in a variable:
  const API_BASE = 'http://localhost:8000';

  let recipeUrl = '';
  let statusMessage = '';
  let resultData = null; // Will store the final result from the server
  let jobId = null;

  async function startEstimation() {
    if (!recipeUrl) {
      statusMessage = 'Please enter a recipe URL.';
      return;
    }
    statusMessage = 'Starting CO2 estimation...';
    resultData = null;

    try {
      const resp = await fetch(`${API_BASE}/estimate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: recipeUrl,
          use_cache: true,
          negligeble_threshold: null
        })
      });
      if (!resp.ok) {
        statusMessage = `Failed to start estimation: ${resp.statusText}`;
        return;
      }
      const data = await resp.json();
      jobId = data.uid;
      statusMessage = 'Estimation in progress...';
      pollStatus();
    } catch (err) {
      statusMessage = `Error: ${err.message}`;
    }
  }

  async function pollStatus() {
    if (!jobId) return;

    try {
      const resp = await fetch(`${API_BASE}/status/${jobId}`);
      if (!resp.ok) {
        statusMessage = `Error fetching status: ${resp.statusText}`;
        return;
      }
      const data = await resp.json();

      if (data.status === 'Processing') {
        // Keep polling
        statusMessage = 'Processing... please wait.';
        setTimeout(pollStatus, 2000);
      } else if (data.status === 'Completed') {
        statusMessage = 'Estimation complete!';
        // The "result" is the JSON string from your `async_estimator`
        // so parse it if necessary
        resultData = JSON.parse(data.result);
      } else if (data.status === 'Error') {
        statusMessage = `Error: ${data.result}`;
      }
    } catch (err) {
      statusMessage = `Error polling status: ${err.message}`;
    }
  }
</script>

<h1>CO2 Estimator</h1>
<div>
  <label for="recipeUrl">Recipe URL:</label>
  <input id="recipeUrl" bind:value={recipeUrl} placeholder="https://example.com" />
  <button on:click={startEstimation}>Estimate CO2</button>
</div>

<p>{statusMessage}</p>

{#if resultData}
  <h2>Estimation Result</h2>
  <pre>{JSON.stringify(resultData, null, 2)}</pre>
{/if}