<script lang="ts">
  import IngredientGrid from "$lib/components/IngredientGrid.svelte";
  import OverviewCard from "$lib/components/OverviewCard.svelte";
  import ReturnHomeButton from "$lib/components/ReturnHomeButton.svelte";
  import { Button, Modal } from "flowbite-svelte";

  /* The loader’s return value arrives here. */
  export let data: { uid: string; result: any };

  let showModal = false;
  let selectedNotes = "";
  let selectedIngredientName = "";

  function openNotes(ing: any) {
    selectedIngredientName = ing.name;
    selectedNotes = `Beregning Noter: ${ing.calculation_notes}
Vægt Estimering Noter: ${ing.weight_estimation_notes}
CO2e Udledning Noter: ${ing.co2_emission_notes}`;
    showModal = true;
  }
</script>

<div class="container mx-auto px-4">
  <div class="mt-4">
    <ReturnHomeButton />
  </div>
  <h2 class="text-xl font-bold mb-4 mt-8">Oversigt</h2>
  <OverviewCard overviewData={data.result} />
  <h2 class="text-xl font-bold mb-4 mt-8">Ingredienser</h2>
  <IngredientGrid
    ingredients={data.result.ingredients}
    onShowNotes={openNotes}
  />
</div>

<Modal bind:open={showModal} on:close={() => (showModal = false)}>
  <div slot="header">
    <h3 class="text-xl font-semibold">{selectedIngredientName}</h3>
  </div>

  <div class="p-6 space-y-2">
    <pre class="text-sm whitespace-pre-wrap">{selectedNotes}</pre>
  </div>

  <div slot="footer" class="flex justify-end p-4">
    <Button on:click={() => (showModal = false)}>Luk</Button>
  </div>
</Modal>
