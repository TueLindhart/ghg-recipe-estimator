<script lang="ts">
  import { Card } from "flowbite-svelte";

  export let co2PerPerson: number;
  export let mealBudget: number;
  export let dayBudget: number;
  export let avgMeal: number;

  $: pctMeal = (co2PerPerson / mealBudget) * 100;
  $: pctDay = (co2PerPerson / dayBudget) * 100;
  $: pctAvg = (co2PerPerson / avgMeal) * 100;
</script>

<Card class="space-y-2 p-4">
  <div>
    <span class="text-2xl font-bold">{pctMeal.toFixed(0)}%</span>
    <span class="text-sm"> af dit budget per måltid på {mealBudget} kg CO2</span>
  </div>
  <div>
    <span class="text-2xl font-bold">{pctDay.toFixed(0)}%</span>
    <span class="text-sm"> af dagligt budget på {dayBudget} kg CO2</span>
  </div>
  <div>
    <span class="text-2xl font-bold">{pctAvg.toFixed(0)}%</span>
    <span class="text-sm"> af en gennemsnitsdanskers måltid på {avgMeal} kg CO2</span>
  </div>
</Card>
