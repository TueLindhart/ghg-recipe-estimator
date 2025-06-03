<script lang="ts">
  /* ───────────────────────── Imports ───────────────────────── */
  import EmissionBarChart  from "$lib/components/EmissionBarChart.svelte";
  import IngredientGrid    from "$lib/components/IngredientGrid.svelte";
  import OverviewCard      from "$lib/components/OverviewCard.svelte";
  import EmissionComparison from "$lib/components/EmissionComparison.svelte";   // NEW
  import ReturnHomeButton  from "$lib/components/ReturnHomeButton.svelte";
  import { Button, Modal, TabItem, Tabs } from "flowbite-svelte";

  /* ───────────────────────── Props ─────────────────────────── */
  export let data: {
    uid: string;
    result: any;
    comparison: {
      input_co2_kg: number;
      reference_kg: number;
      ratio: number;
      helperText: string;
    };
  };

  /* ───────────────────────── Local state ───────────────────── */
  let showModal            = false;
  let selectedNotes        = "";
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

  <h2 class="text-xl font-bold mb-4 mt-4">Oversigt</h2>

  <!-- ───── Overview + Comparison side-by-side ───── -->
  <div class="flex flex-col lg:flex-row gap-6 mb-8">
    <OverviewCard
      class="flex-1"
      overviewData={data.result}
    />

    <EmissionComparison
      kgco2       ={data.result.co2_per_person_kg}
      referenceKg ={data.comparison.reference_kg}
      ratio       ={data.comparison.ratio}
      helperText  ={data.comparison.helperText}
    />
  </div>

  <!-- ───── Tabs (unchanged) ───── -->
  <Tabs class="mt-8" tabStyle="pill">
    <TabItem title="Ingredienser" open>
      <div class="min-h-[300px] max-h-[400px] md:max-h-[400px] overflow-y-auto">
        <IngredientGrid
          ingredients={data.result.ingredients}
          onShowNotes={openNotes}
        />
      </div>
    </TabItem>

    <TabItem title="Graf">
      <div class="min-h-[300px] max-h-[400px] md:max-h-[400px] overflow-y-auto">
        <EmissionBarChart ingredients={data.result.ingredients} />
      </div>
    </TabItem>
  </Tabs>
</div>

<!-- ───── Notes Modal (unchanged) ───── -->
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