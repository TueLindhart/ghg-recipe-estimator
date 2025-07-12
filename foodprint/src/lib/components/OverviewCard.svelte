<!-- OverviewCard.svelte -->
<script lang="ts">
  import { Card } from "flowbite-svelte";
  import type { RecipeCO2Output } from "$lib";

  export let overviewData: RecipeCO2Output;
</script>

<Card class="!max-w-none w-full md:w-1/2 bg-white border border-gray-200 rounded-lg shadow p-6 flex flex-col items-center">
  <span class="text-4xl md:text-6xl font-extrabold tracking-tight text-gray-900">
    {overviewData.co2_per_person_kg?.toLocaleString()} kg CO2e
  </span>
  <span class="mt-2 text-sm text-gray-700">
    {overviewData.total_co2_kg} kg CO2e for {overviewData.number_of_persons} personer
  </span>
</Card>
