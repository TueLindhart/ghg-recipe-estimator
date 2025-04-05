<script>
  import { Card, Button } from 'flowbite-svelte';
  export let ingredient;
  export let onShowNotes; // Callback to show notes modal
</script>

<Card class="p-4">
  <h3 class="text-md font-semibold mb-1">{ingredient.name}</h3>
  <p class="text-sm">Vægt: {ingredient.weight_kg} kg</p>
  <p class="text-sm">Udledning pr. kg: {ingredient.co2_per_kg} kg CO2e/kg</p>
  <p class="text-sm mb-2">Udledning: {ingredient.co2_kg} kg</p>
  <Button on:click={() => onShowNotes(ingredient)}>Vis Noter</Button>
</Card>