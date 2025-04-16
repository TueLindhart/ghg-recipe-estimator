<script>
  import { TabItem, Tabs } from "flowbite-svelte";

  export let ingredients = [];
  export let onShowNotes;

  // Group ingredients by category
  $: groupedIngredients = ingredients.reduce((acc, ingredient) => {
    const category = ingredient.category || "Andre";
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(ingredient);
    return acc;
  }, {});

  export let tabs = [
    /* Expected format:
    {
      name: "Tab Name",
      component: SvelteComponent,
      props: {}, // Optional props to pass to the component
      open: false // Optional, defaults to false
    }
    */
  ];
</script>

<Tabs style="underline">
  {#each tabs as tab, i}
    <TabItem open={tab.open || i === 0} title={tab.name}>
      <svelte:component this={tab.component} {...tab.props || {}} />
    </TabItem>
  {/each}
</Tabs>
