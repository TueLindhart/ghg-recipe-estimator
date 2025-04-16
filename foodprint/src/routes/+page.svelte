<script>
  import IngredientGrid from "$lib/components/IngredientGrid.svelte";
  import InputBar from "$lib/components/InputBar.svelte";
  import OverviewForm from "$lib/components/OverviewForm.svelte";
  import ProgressBar from "$lib/components/ProgressBar.svelte";
  import { Button, Modal } from "flowbite-svelte";

  let recipeUrl = "";
  let statusMessage = "";
  let resultData = null; // Holds the API result data
  let jobId = null; // Unique job id returned by FastAPI
  let isProcessing = false; // Controls whether the progress bar is shown
  let status = ""; // Status of the estimation process

  // Modal state for showing ingredient notes
  let showModal = false;
  let selectedNotes = "";

  // Update recipeUrl on input change
  function handleInputChange(val) {
    recipeUrl = val;
  }

  // Start the estimation process
  async function startEstimation() {
    if (!recipeUrl) {
      statusMessage = "Angiv venligst en URL.";
      return;
    }
    isProcessing = true;
    resultData = null;
    try {
      const resp = await fetch(`/api/estimate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: recipeUrl,
        }),
      });
      if (!resp.ok) {
        statusMessage = `Fejl ved start af estimering: ${resp.statusText}`;
        isProcessing = false;
        return;
      }
      const data = await resp.json();
      jobId = data.uid;
      pollStatus();
    } catch (err) {
      statusMessage = `Fejl: ${err.message}`;
      isProcessing = false;
    }
  }

  // Poll the status endpoint until the estimation completes
  async function pollStatus() {
    if (!jobId) return;
    try {
      const resp = await fetch(`/api/status/${jobId}`);
      if (!resp.ok) {
        statusMessage = `Fejl ved statusopdatering: ${resp.statusText}`;
        isProcessing = false;
        return;
      }
      const data = await resp.json();
      status = data.status;

      switch (status) {
        case "Processing":
          statusMessage = "Behandler opskrift...";
          setTimeout(pollStatus, 2000);
          break;
        case "Completed":
          resultData = JSON.parse(data.result);
          statusMessage = "";
          isProcessing = false;
          break;
        case "Error":
          statusMessage = `Fejl: ${data.result}`;
          isProcessing = false;
          break;
        case "Text":
          statusMessage = "Henter opskrift fra URL...";
          setTimeout(pollStatus, 2000);
          break;
        case "Recipe":
          statusMessage = "Udtrækker ingredienser...";
          setTimeout(pollStatus, 2000);
          break;
        case "Weights":
          statusMessage = "Estimerer vægt per ingrediens...";
          setTimeout(pollStatus, 2000);
          break;
        case "RAGCO2":
          statusMessage = "Estimerer CO2 udledning per ingrediens...";
          setTimeout(pollStatus, 2000);
          break;
        case "Preparing":
          statusMessage = "Forbereder resultater...";
          setTimeout(pollStatus, 2000);
          break;
        default:
          statusMessage = `Ukendt status: ${data.status}`;
          isProcessing = false;
      }
    } catch (err) {
      statusMessage = `Fejl ved polling: ${err.message}`;
      isProcessing = false;
    }
  }

  // Open modal to display ingredient notes
  function showNotes(ingredient) {
    selectedNotes = `Beregning Noter: ${ingredient.calculation_notes}
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

  <!-- Separate Progress Bar -->
  {#if isProcessing && !resultData}
    <ProgressBar {status} />
  {/if}

  <!-- Status Message - only show for errors -->
  {#if statusMessage && statusMessage.includes("Fejl")}
    <p class="text-lg mb-4 text-red-600">{statusMessage}</p>
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
      <IngredientGrid
        ingredients={resultData.ingredients}
        onShowNotes={showNotes}
      />
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
