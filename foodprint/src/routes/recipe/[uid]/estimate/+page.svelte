<script lang="ts">
  import EmissionBarChart from "$lib/components/EmissionBarChart.svelte";
  import IngredientGrid from "$lib/components/IngredientGrid.svelte";
  import OverviewCard from "$lib/components/OverviewCard.svelte";
  import ReturnHomeButton from "$lib/components/ReturnHomeButton.svelte";
  import { Button, Modal, TabItem, Tabs } from "flowbite-svelte";

  export let data: { uid: string; result: any };

  // Compute full URL and display domain from data.result.url if available
  let domainFull = "";
  let domainDisplay = "";
  if (data.result.url) {
    const parsedUrl = new URL(data.result.url);
    domainFull = parsedUrl.href;
    domainDisplay = parsedUrl.hostname
      .replace(/^www\./, "")
      .replace(/\.[^.]*$/, "");
  }

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
  <div class="mt-4 flex items-center gap-4">
    <ReturnHomeButton />
    {#if data.result.url}
      <!-- Modified URL display: Button without blue url styling -->
      <Button on:click={() => window.open(data.result.url, "_blank")}>
        {"Gå til opskrift"}
      </Button>
    {/if}
    {#if data.result.title}
      <h1 class="text-2xl">
        <span class="font-bold">{data.result.title}</span> af {domainDisplay}
      </h1>
    {/if}
  </div>

  <h2 class="text-xl font-bold mb-4 mt-4">Oversigt</h2>
  <OverviewCard overviewData={data.result} />

  <!-- Wrapper div to enforce bottom spacing -->
  <div class="mb-8">
    <Tabs class="mt-8" tabStyle="pill">
      <TabItem title="Ingredienser" open>
        <div
          class="min-h-[300px] max-h-[400px] md:max-h-[400px] overflow-y-auto"
        >
          <IngredientGrid
            ingredients={data.result.ingredients}
            onShowNotes={openNotes}
          />
        </div>
      </TabItem>

      <TabItem title="Graf">
        <div
          class="min-h-[300px] max-h-[400px] md:max-h-[400px] overflow-y-auto"
        >
          <EmissionBarChart ingredients={data.result.ingredients} />
        </div>
      </TabItem>
    </Tabs>
  </div>
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
