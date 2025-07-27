<script lang="ts">
  import { Card } from "flowbite-svelte";
  import NutritionChart from "./NutritionChart.svelte";

  export let energyPerPersonKj: number;
  export let caloriesPerPersonKcal: number;
  export let fatPerPersonG: number;
  export let carbohydratePerPersonG: number;
  export let proteinPerPersonG: number;
  export let cardClass = "";
</script>

<Card class={cardClass}>
  <!-- Main content container with consistent height -->
  <div class="flex flex-col h-full min-h-0 lg:min-h-52">
    <!-- Centered container for nutrition content -->
    <div class="flex-grow flex items-center justify-center">
      <div class="flex flex-col lg:flex-row items-center justify-center gap-6">
        <div class="text-center space-y-3 lg:space-y-4">
          <div>
            <span class="text-3xl font-bold text-[#404040]">
              {energyPerPersonKj} kJ
            </span>
            <div class="text-sm text-gray-600 mt-1">Energi pr. person</div>
          </div>
          <div>
            <span class="text-2xl font-bold text-[#404040]">
              {caloriesPerPersonKcal} kcal
            </span>
            <div class="text-sm text-gray-600 mt-1">Kalorier pr. person</div>
          </div>
        </div>
        <div class="flex-1 w-full lg:w-auto">
          <NutritionChart
            fat={fatPerPersonG}
            carbohydrate={carbohydratePerPersonG}
            protein={proteinPerPersonG}
          />
        </div>
      </div>
    </div>
  </div>
</Card>
