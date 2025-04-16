<script lang="ts">
  import IngredientGrid from "$lib/components/IngredientGrid.svelte";
  import InputBar from "$lib/components/InputBar.svelte";
  import OverviewForm from "$lib/components/OverviewForm.svelte";
  import ProgressBar from "$lib/components/ProgressBar.svelte";
  import { Button, Modal } from "flowbite-svelte";

  let recipeUrl = "";
  let statusMessage = "";
  let resultData: any = null;
  let jobId: string | null = null;
  let isProcessing = false;

  let showModal = false;
  let selectedNotes = "";

  function handleInputChange(val: string) {
    recipeUrl = val;
  }

  /** call server action ?/startEstimation */
  async function startEstimation(): Promise<void> {
    if (!recipeUrl) {
      statusMessage = "Angiv venligst en URL.";
      return;
    }

    isProcessing = true;
    resultData = null;

    const form = new FormData();
    form.set("url", recipeUrl);
    const resp = await fetch("?/startEstimation", {
      method: "POST",
      headers: { accept: "application/json" },
      body: form,
    });
    const { type, data: payload } = await resp.json();

    if (type === "error") {
      +   statusMessage = payload?.error ?? resp.statusText;
      isProcessing = false;
      return;
    }

    jobId = data.jobId;
    pollStatus();
  }

  /** call server action ?/pollStatus every 2 s until done */
  async function pollStatus(): Promise<void> {
    if (!jobId) return;

    const form = new FormData();
    form.set("jobId", jobId);
    const resp = await fetch("?/pollStatus", {
      method: "POST",
      headers: { accept: "application/json", "x-sveltekit-action": "true" },
      body: form,
    });

    const data = await resp.json();

    if (!resp.ok || data.error) {
      statusMessage = data.error ?? resp.statusText;
      isProcessing = false;
      return;
    }

    switch (data.status) {
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
  }

  function showNotes(ingredient: any): void {
    selectedNotes = `Beregning Noter: ${ingredient.calculation_notes}
Vægt Estimering Noter: ${ingredient.weight_estimation_notes}
CO2e Udledning Noter: ${ingredient.co2_emission_notes}`;
    showModal = true;
  }
</script>

<div class="container mx-auto px-4 flex flex-col items-center">
  <!-- Input Bar Component -->
  <div class="w-full max-w-2xl">
    <InputBar
      {recipeUrl}
      onInputChange={handleInputChange}
      onButtonClick={startEstimation}
    />
  </div>

  <!-- Separate Progress Bar -->
  {#if isProcessing && !resultData}
    <div class="w-full max-w-2xl">
      <ProgressBar />
    </div>
  {/if}

  <!-- Status Message -->
  {#if statusMessage}
    <p class="text-lg mb-4 text-center">{statusMessage}</p>
  {/if}

  {#if resultData}
    <!-- Overview Section -->
    <div class="w-full max-w-2xl mb-6">
      <h2 class="text-xl font-bold mb-2 text-center">Oversigt</h2>
      <OverviewForm overviewData={resultData} />
    </div>

    <!-- Ingredients Section -->
    <div class="w-full max-w-4xl">
      <h2 class="text-xl font-bold mb-2 text-center">Ingredienser</h2>
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
