<script lang="ts">
  import { Card } from "flowbite-svelte";
  import { InfoCircleOutline } from "flowbite-svelte-icons";

  import type { IngredientOutput } from "$lib";

  export let ingredient: IngredientOutput;
  export let onShowNotes: (ing: IngredientOutput) => void;
</script>

<Card class="p-4 relative">

  <!-- Info icon in the top-right corner -->
  <button
    class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 focus:outline-none"
    on:click={() => onShowNotes(ingredient)}
    aria-label="Vis noter"
  >
    <InfoCircleOutline class="w-5 h-5" />
  </button>

  <h3 class="text-md font-semibold mb-1 text-[#404040]">
    {ingredient.name}
  </h3>

  <p class="text-sm mb-1">
    <span class="font-semibold">Udledning:</span>
    {ingredient.co2_kg != null ? `${ingredient.co2_kg} kg CO2e` : "-"}
  </p>

  <p class="text-sm mb-1">
    <span class="font-semibold">Vægt:</span>
    {ingredient.weight_kg != null ? `${ingredient.weight_kg} kg` : "-"}
  </p>

  <p class="text-sm">
    <span class="font-semibold">Udledning pr. kg:</span>
    {ingredient.co2_per_kg != null
      ? `${ingredient.co2_per_kg} kg CO2e/kg`
      : "-"}
  </p>

  <p class="text-sm">
    <span class="font-semibold">Energi:</span>
    {ingredient.energy_kj != null ? `${ingredient.energy_kj} kJ` : "-"}
  </p>
  <p class="text-sm">
    <span class="font-semibold">Fedt:</span>
    {ingredient.fat_g != null ? `${ingredient.fat_g} g` : "-"}
  </p>
  <p class="text-sm">
    <span class="font-semibold">Kulhydrat:</span>
    {ingredient.carbohydrate_g != null ? `${ingredient.carbohydrate_g} g` : "-"}
  </p>
  <p class="text-sm">
    <span class="font-semibold">Protein:</span>
    {ingredient.protein_g != null ? `${ingredient.protein_g} g` : "-"}
  </p>
</Card>