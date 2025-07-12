<!-- OverviewCard.svelte -->
<script lang="ts">
  import type { RecipeCO2Output } from "$lib";
  import { Card } from "flowbite-svelte";

  export let overviewData: RecipeCO2Output;
</script>

<Card
  class="!max-w-none w-full md:w-1/2 lg:w-1/3 bg-white border border-gray-200 rounded-lg shadow p-6 flex flex-col justify-between h-64"
>
  <div class="flex flex-col items-center justify-center flex-1">
    <span
      class="text-6xl md:text-[6rem] font-extrabold tracking-tight text-gray-900"
    >
      {overviewData.co2_per_person_kg?.toLocaleString()}
    </span>
    <span class="text-2xl font-bold text-gray-900 -mt-2"
      >kg CO2e pr. person</span
    >
  </div>
  <div class="flex items-center justify-center">
    <span class="text-xl text-gray-900 mb-2">
      {overviewData.total_co2_kg} kg co2e for {overviewData.number_of_persons} personer
    </span>
  </div>
</Card>
