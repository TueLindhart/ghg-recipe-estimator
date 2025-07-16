<script lang="ts">
  import BaseButton from "$lib/components/BaseButton.svelte";
  import BudgetComparison from "$lib/components/BudgetComparison.svelte";
  import EmissionBarChart from "$lib/components/EmissionBarChart.svelte";
  import EquivalentComparison from "$lib/components/EquivalentComparison.svelte";
  import IngredientGrid from "$lib/components/IngredientGrid.svelte";
  import NutritionChart from "$lib/components/NutritionChart.svelte";
  import OverviewCard from "$lib/components/OverviewCard.svelte";
  import ReturnHomeButton from "$lib/components/ReturnHomeButton.svelte";

  import type { IngredientOutput } from "$lib";
  import { Button, Modal, TabItem, Tabs } from "flowbite-svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

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

  function openNotes(ing: IngredientOutput) {
    selectedIngredientName = ing.name;
    selectedNotes = `Beregning Noter: ${ing.calculation_notes}
Vægt Estimering Noter: ${ing.weight_estimation_notes}
CO2e Udledning Noter: ${ing.co2_emission_notes}`;
    showModal = true;
  }

  let chartMetric: "co2" | "energy" | "protein" | "carbohydrate" | "fat" =
    "co2";
</script>

<svelte:head>
  <title
    >{data.result.title
      ? `${data.result.title} - MyFoodprint`
      : "MyFoodprint"}</title
  >
</svelte:head>

<div class="container mx-auto px-4">
  <div class="mt-4 flex flex-wrap items-center gap-4">
    <ReturnHomeButton />

    {#if data.result.url}
      <BaseButton
        ariaLabel="Gå til opskrift"
        onClick={() => window.open(data.result.url, "_blank")}
      >
        Gå til opskrift
      </BaseButton>
    {/if}

    {#if data.result.title}
      <!-- “basis-full” makes the h1 start on its own line below 640 px;
         from the sm breakpoint up it behaves like normal inline content -->
      <h1 class="text-2xl basis-full sm:basis-auto">
        <span class="font-bold">{data.result.title}</span> af {domainDisplay}
      </h1>
    {/if}
  </div>

  <!-- Maintain spacing where "Oversigt" was removed -->
  <div class="mb-4 mt-8"></div>

  <!-- ───── Overview with info tabs (Tabs left, content right) ───── -->
  <div class="mb-8 flex flex-col lg:flex-row gap-6">
    <OverviewCard
      overviewData={data.result}
      avgMeal={data.comparison.avg_emission_per_person_per_meal}
    />
    <div class="flex flex-col justify-between">
      <Tabs tabStyle="pill">
        <TabItem title="Sammenlign" open>
          <BudgetComparison
            co2PerPerson={data.result.co2_per_person_kg ?? 0}
            mealBudget={data.result.budget_emission_per_person_per_meal}
            dayBudget={data.result.budget_emission_per_person_per_day}
            avgMeal={data.result.avg_emission_per_person_per_meal}
          />
        </TabItem>
        <TabItem title="Svare til">
          <EquivalentComparison
            co2PerPerson={data.result.co2_per_person_kg ?? 0}
          />
        </TabItem>
        <TabItem title="Næringsindhold">
          <div class="flex items-center gap-4">
            <span class="text-3xl font-bold">
              {data.result.energy_per_person_kj ?? 0} kJ
            </span>
            <NutritionChart
              fat={data.result.fat_per_person_g ?? 0}
              carbohydrate={data.result.carbohydrate_per_person_g ?? 0}
              protein={data.result.protein_per_person_g ?? 0}
            />
          </div>
        </TabItem>
      </Tabs>
    </div>
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
      <div
        class="min-h-[300px] max-h-[400px] md:max-h-[400px] overflow-y-auto space-y-2"
      >
        <select bind:value={chartMetric} class="border rounded p-1">
          <option value="co2">CO2e kg</option>
          <option value="energy">Energi kJ</option>
          <option value="protein">Protein g</option>
          <option value="carbohydrate">Kulhydrat g</option>
          <option value="fat">Fedt g</option>
        </select>
        <EmissionBarChart
          ingredients={data.result.ingredients}
          metric={chartMetric}
        />
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
