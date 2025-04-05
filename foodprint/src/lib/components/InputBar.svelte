<script>
    import { Card, Button } from 'flowbite-svelte';
    import { ArrowRightOutline } from 'flowbite-svelte-icons';
    
    export let recipeUrl = '';
    export let onInputChange = () => {};
    export let onButtonClick = () => {};
  </script>
  
  <Card class="mb-6 p-6">
    <div class="flex flex-col gap-4">
      <div>
        <label for="urlInput" class="block text-lg font-medium text-gray-900 dark:text-white">
          Indtast opskrift URL:
        </label>
        <input
          id="urlInput"
          value={recipeUrl}
          on:input={(e) => onInputChange(e.target.value)}
          placeholder="https://example.com/din-opskrift"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        />
      </div>
      <Button on:click={onButtonClick} class="w-fit">
        Beregn CO2 Emission <ArrowRightOutline class="w-5 h-5 ml-2" />
      </Button>
    </div>
  </Card>