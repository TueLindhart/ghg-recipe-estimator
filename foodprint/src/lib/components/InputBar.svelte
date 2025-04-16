<!-- InputBar.svelte -->
<script>
  import { Button, Card } from "flowbite-svelte";
  import { ArrowRightOutline } from "flowbite-svelte-icons";

  export let recipeUrl = "";
  export let onInputChange = () => {};
  export let onButtonClick = () => {};
</script>

<!-- Center the card and cap its max width -->
<Card class="mb-6 p-6 mx-auto max-w-lg">
  <div class="flex flex-col gap-4">
    <div>
      <label
        for="urlInput"
        class="block text-lg font-medium text-gray-900 dark:text-white"
      >
        Indtast opskrift URL:
      </label>
      <input
        id="urlInput"
        value={recipeUrl}
        on:input={(e) => onInputChange(e.target.value)}
        placeholder="https://example.com/din-opskrift"
        class="
          mt-1
          block
          w-full
          py-3 /* taller input */
          px-4
          text-lg /* larger text */
          rounded-lg /* slightly more rounded */
          border-gray-300
          shadow-sm
          focus:outline-none
          focus:border-indigo-500
          focus:ring-2
          focus:ring-indigo-500
        "
      />
    </div>
    <Button on:click={onButtonClick} class="w-fit">
      Beregn CO2 Emission
      <ArrowRightOutline class="w-5 h-5 ml-2" />
    </Button>
  </div>
</Card>
