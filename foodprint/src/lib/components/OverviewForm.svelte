<script>
  import { Card } from "flowbite-svelte";
  export let overviewData;
</script>

<Card>
  <form class="grid grid-cols-2 gap-4">
    <!-- Total CO2 -->
    <div>
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">
        Total CO2 (kg)
      </label>
      <input
        type="text"
        value={overviewData.total_co2_kg}
        readonly
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      />
    </div>

    <!-- CO2 per Person -->
    <div>
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">
        CO2 per Person (kg)
      </label>
      <input
        type="text"
        value={overviewData.co2_per_person_kg}
        readonly
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      />
    </div>

    <!-- Personer -->
    <div>
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">
        Personer
      </label>
      <input
        type="text"
        value={overviewData.number_of_persons}
        readonly
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      />
    </div>

    <!-- Gennemsnit Range -->
    <div>
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">
        Gennemsnit (kg)
      </label>
      <input
        type="text"
        value={`${overviewData.avg_meal_emission_per_person_range_kg[0]} - ${overviewData.avg_meal_emission_per_person_range_kg[1]}`}
        readonly
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      />
    </div>
  </form>
</Card>
