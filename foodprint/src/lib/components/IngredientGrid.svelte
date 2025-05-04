<script>
  import IngredientCard from "./IngredientCard.svelte";
  export let ingredients = [];
  export let onShowNotes;
</script>

<!-- mobile: 1 col · ≥md (≥768 px): 3 cols -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-2">
  {#each ingredients as ingredient}
    <IngredientCard {ingredient} {onShowNotes} />
  {/each}
</div>
