<script>
  import { Button, Card } from "flowbite-svelte";
  export let ingredient;
  export let onShowNotes; // Callback to show notes modal
</script>

<Card class="p-4">
  <h3 class="text-md font-semibold mb-1 text-[#404040]">{ingredient.name}</h3>
  <p class="text-sm mb-1">
    <span class="font-semibold">Udledning:</span>
    {ingredient.co2_kg != null ? `${ingredient.co2_kg} kg CO2e` : "-"}
  </p>
  <p class="text-sm mb-1">
    <span class="font-semibold">Vægt:</span>
    {ingredient.weight_kg != null ? `${ingredient.weight_kg} kg` : "-"}
  </p>
  <p class="text-sm mb-2">
    <span class="font-semibold">Udledning pr. kg:</span>
    {ingredient.co2_per_kg != null
      ? `${ingredient.co2_per_kg} kg CO2e/kg`
      : "-"}
  </p>
  <Button on:click={() => onShowNotes(ingredient)}>Vis Noter</Button>
</Card>
