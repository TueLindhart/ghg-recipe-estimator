<script>
  import { onMount } from 'svelte';
  import InputBar from '$lib/components/InputBar.svelte';
  import OverviewForm from '$lib/components/OverviewForm.svelte';
  import IngredientGrid from '$lib/components/IngredientGrid.svelte';
  import { Modal, Button } from 'flowbite-svelte';

  // Set your FastAPI backend URL
  const API_BASE = 'http://localhost:8000';

  let recipeUrl = '';
  let statusMessage = '';
  let resultData = null;  // Holds the API result data
  let jobId = null;       // Unique job id returned by FastAPI

  // Modal state for showing ingredient notes
  let showModal = false;
  let selectedNotes = '';

  // Update recipeUrl on input change
  function handleInputChange(val) {
    recipeUrl = val;
  }

  // Start the estimation process
  async function startEstimation() {
    if (!recipeUrl) {
      statusMessage = 'Angiv venligst en URL.';
      return;
    }
    statusMessage = 'Beregner CO2-udledning...';
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
        statusMessage = `Fejl ved start af estimering: ${resp.statusText}`;
        return;
      }
      const data = await resp.json();
      jobId = data.uid;
      statusMessage = 'Estimering påbegyndt...';
      pollStatus();
    } catch (err) {
      statusMessage = `Fejl: ${err.message}`;
    }
  }

  // Poll the status endpoint until the estimation completes
  async function pollStatus() {
    if (!jobId) return;
    try {
      const resp = await fetch(`${API_BASE}/status/${jobId}`);
      if (!resp.ok) {
        statusMessage = `Fejl ved statusopdatering: ${resp.statusText}`;
        return;
      }
      const data = await resp.json();
      if (data.status === 'Processing') {
        statusMessage = 'Arbejder stadig på det...';
        setTimeout(pollStatus, 2000);
      } else if (data.status === 'Completed') {
        statusMessage = 'Estimering fuldført!';
        resultData = JSON.parse(data.result);
      } else if (data.status === 'Error') {
        statusMessage = `Fejl: ${data.result}`;
      }
    } catch (err) {
      statusMessage = `Fejl ved polling: ${err.message}`;
    }
  }

  // Open modal to display ingredient notes
  function showNotes(ingredient) {
    selectedNotes = 
`Beregning Noter: ${ingredient.calculation_notes}
Vægt Estimering Noter: ${ingredient.weight_estimation_notes}
CO2e Udledning Noter: ${ingredient.co2_emission_notes}`;
    showModal = true;
  }
</script>

<div class="container mx-auto px-4">
  <!-- Input Bar Component -->
  <InputBar
    {recipeUrl}
    onInputChange={handleInputChange}
    onButtonClick={startEstimation}
  />

  <!-- Status Message -->
  {#if statusMessage}
    <p class="text-lg mb-4">{statusMessage}</p>
  {/if}

  {#if resultData}
    <!-- Overview Section -->
    <div class="mb-6">
      <h2 class="text-xl font-bold mb-2">Oversigt</h2>
      <OverviewForm overviewData={resultData} />
    </div>

    <!-- Ingredients Section -->
    <div>
      <h2 class="text-xl font-bold mb-2">Ingredienser</h2>
      <IngredientGrid ingredients={resultData.ingredients} onShowNotes={showNotes} />
    </div>
  {/if}
</div>

<!-- Modal for showing ingredient notes -->
<Modal show={showModal} on:close={() => (showModal = false)}>
  <div slot="header">
    <h3 class="text-xl font-semibold">Noter</h3>
  </div>
  <div class="p-6 space-y-2">
    <pre class="text-sm whitespace-pre-wrap">{selectedNotes}</pre>
  </div>
  <div slot="footer" class="flex justify-end p-4">
    <Button color="gray" on:click={() => (showModal = false)}>Luk</Button>
  </div>
</Modal>