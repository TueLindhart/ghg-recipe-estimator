<script lang="ts">
  // Sørg for lang="ts" hvis du bruger TypeScript her
  import { Button, Card } from "flowbite-svelte";
  import { ArrowRightOutline } from "flowbite-svelte-icons";

  export let recipeUrl: string = "";
  // Forventer en funktion der tager en string som argument
  export let onInputChange: (value: string) => void = () => {};
  export let onButtonClick: () => void = () => {};
</script>

<Card class="mb-6 p-6 w-full max-w-xl mx-auto">
  <div class="flex flex-col gap-4 items-center">
    <div class="w-full flex items-center gap-4">
      <div class="flex-1">
        <input
          id="urlInput"
          type="url"
          value={recipeUrl}
          on:input={(e) => onInputChange((e.target as HTMLInputElement).value)}
          placeholder="https://eksempel.dk/din-opskrift"
          class="block w-full h-12 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          required
        />
      </div>
      <Button on:click={onButtonClick} size="lg" class="h-12">
        <ArrowRightOutline class="w-5 h-5 ml-2 self-center" />
      </Button>
    </div>
  </div>
</Card>
