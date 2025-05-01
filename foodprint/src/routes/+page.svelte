<script>
  import { enhance } from "$app/forms";
  import IngredientGrid from "$lib/components/IngredientGrid.svelte";
  import InputBar from "$lib/components/InputBar.svelte";
  import OverviewForm from "$lib/components/OverviewForm.svelte";
  import ProgressBar from "$lib/components/ProgressBar.svelte";
  import { Button, Modal } from "flowbite-svelte";

  let recipeUrl = "";
  let statusMessage = "";
  let resultData = null; // API-resultat
  let isProcessing = false; // Styrer progress-bar
  let status = ""; // Simpel status-streng

  // Modal-state
  let showModal = false;
  let selectedNotes = "";

  function handleInputChange(val) {
    recipeUrl = val;
  }

  /* ---------- Svelte-Kit action helpers ---------- */
  const enhanceOpts = {
    pending: () => {
      isProcessing = true;
      statusMessage = "";
      status = "Processing";
      resultData = null;
    },
    error: (_e, { error }) => {
      isProcessing = false;
      statusMessage = error;
      status = "Error";
    },
    result: (_e, { result }) => {
      isProcessing = false;
      status = "Completed";
      resultData = result;
    },
  };

  /* ---------- Modal helpers ---------- */
  function showNotes(ingredient) {
    selectedNotes = `Beregning Noter: ${ingredient.calculation_notes}
  Vægt Estimering Noter: ${ingredient.weight_estimation_notes}
  CO2e Udledning Noter: ${ingredient.co2_emission_notes}`;
    showModal = true;
  }
</script>

<div class="container mx-auto px-4">
  <!-- Hele siden er nu ét form der POST'er til +page.server.ts -->
  <form method="POST" use:enhance={enhanceOpts}>
    <!-- Input Bar -->
    <InputBar {recipeUrl} onInputChange={handleInputChange} />

    <!-- Progress Bar -->
    {#if isProcessing && !resultData}
      <ProgressBar {status} />
    {/if}

    <!-- Fejlbeskeder -->
    {#if statusMessage && status === "Error"}
      <p class="text-lg mb-4 text-red-600">{statusMessage}</p>
    {/if}

    <!-- Resultater -->
    {#if resultData}
      <div class="mb-6">
        <h2 class="text-xl font-bold mb-2">Oversigt</h2>
        <OverviewForm overviewData={resultData} />
      </div>

      <div>
        <h2 class="text-xl font-bold mb-2">Ingredienser</h2>
        <IngredientGrid
          ingredients={resultData.ingredients}
          onShowNotes={showNotes}
        />
      </div>
    {/if}
  </form>
</div>

<!-- Modal til noter -->
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
