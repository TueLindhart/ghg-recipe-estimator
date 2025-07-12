<!-- OverviewCard.svelte -->
<script lang="ts">
  import { Card } from "flowbite-svelte";

  import type { RecipeCO2Output } from "$lib";

  export let overviewData: RecipeCO2Output;
  export let avgMeal: number;

  type Stat = { label: string; value: string; unit?: string };

  const stats: Stat[] = [
    {
      label: "Total CO₂",
      value: overviewData.total_co2_kg.toLocaleString(),
      unit: "kg",
    },
    {
      label: "CO₂ pr. person",
      value: overviewData.co2_per_person_kg.toLocaleString(),
      unit: "kg",
    },
    { label: "Personer", value: overviewData.number_of_persons.toString() },
    {
      label: "Gennemsnit pr. måltid",
      value: `${avgMeal.toString()}`,
      unit: "kg",
    },
  ];
</script>

<!-- Remove the default max‑w‑sm cap, then set width -->
<Card
  class="!max-w-none w-full md:w-1/2 bg-white border border-gray-200 rounded-lg shadow"
>
  <div class="grid grid-cols-2 grid-rows-2">
    {#each stats as { value, unit, label }}
      <div class="flex flex-col items-center justify-center p-6">
        <span
          class="text-2xl md:text-3xl font-extrabold tracking-tight text-gray-900"
        >
          {value}{unit ? ` ${unit}` : ""}
        </span>
        <span
          class="mt-1 text-sm font-medium text-gray-500 uppercase tracking-wide"
        >
          {label}
        </span>
      </div>
    {/each}
  </div>
</Card>
