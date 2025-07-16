<script lang="ts">
  import { Button, Card, Modal } from "flowbite-svelte";
  import { InfoCircleOutline } from "flowbite-svelte-icons";

  export let co2PerPerson: number;
  export let mealBudget: number;
  export let dayBudget: number;
  export let avgMeal: number;
  export let cardClass = "max-w-full";

  $: pctMeal = (co2PerPerson / mealBudget) * 100;
  $: pctDay = (co2PerPerson / dayBudget) * 100;
  $: pctAvg = (co2PerPerson / avgMeal) * 100;

  let showModal = false;
</script>

<Card class="p-4 relative {cardClass}">
  <!-- Info icon in the top-right corner -->
  <button
    class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 focus:outline-none"
    on:click={() => (showModal = true)}
    aria-label="Vis budget detaljer"
  >
    <InfoCircleOutline class="w-5 h-5" />
  </button>

  <!-- Budget comparisons in horizontal layout -->
  <div class="flex justify-center items-center gap-12 mb-4">
    <div class="flex flex-col items-center">
      <span class="text-2xl font-bold">{pctMeal.toFixed(0)}%</span>
      <span class="text-sm mt-1">måltid budget</span>
    </div>
    <div class="flex flex-col items-center">
      <span class="text-2xl font-bold">{pctDay.toFixed(0)}%</span>
      <span class="text-sm mt-1">dagligt budget</span>
    </div>
  </div>

  <!-- Average person comparison -->
  <p class="text-xs text-gray-600">
    Gennemsnitsdansker udleder {avgMeal} CO2e per måltid
  </p>
</Card>

<!-- Modal with budget details -->
<Modal bind:open={showModal}>
  <div slot="header">
    <h3 class="text-xl font-semibold">Budget Detaljer</h3>
  </div>
  <div class="p-6 space-y-4">
    <p>
      <span class="font-semibold">Måltid budget:</span>
      {mealBudget} kg CO2
    </p>
    <p>
      <span class="font-semibold">Dagligt budget:</span>
      {dayBudget} kg CO2
    </p>
  </div>
  <div slot="footer" class="flex justify-end">
    <Button on:click={() => (showModal = false)}>Luk</Button>
  </div>
</Modal>
