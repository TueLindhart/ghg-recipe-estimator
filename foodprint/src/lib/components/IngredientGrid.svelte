<script>
  import IngredientCard from "./IngredientCard.svelte";
  export let ingredients = [];
  export let onShowNotes;
</script>

<div class="grid grid-cols-3 gap-2">
  {#each ingredients as ingredient}
    <IngredientCard {ingredient} {onShowNotes} />
  {/each}
</div>
