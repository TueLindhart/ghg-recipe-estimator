<script lang="ts">
  import IngredientCard from "./IngredientCard.svelte";
  import type { IngredientOutput } from "$lib";
  export let ingredients: IngredientOutput[] = [];
  export let onShowNotes: (ing: IngredientOutput) => void;
</script>

<!-- mobile: 1 col · ≥md (≥768 px): 3 cols -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-2">
  {#each ingredients as ingredient}
    <IngredientCard {ingredient} {onShowNotes} />
  {/each}
</div>
