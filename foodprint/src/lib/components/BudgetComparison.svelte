<script lang="ts">
  import { Button, Card, Modal } from "flowbite-svelte";
  import { InfoCircleOutline } from "flowbite-svelte-icons";
  import ThermometerChart from "./ThermometerChart.svelte";

  export let co2PerPerson: number;
  export let mealBudget: number;
  export let dayBudget: number;
  export let avgMeal: number;
  export let cardClass = "";

  $: pctMeal = (co2PerPerson / mealBudget) * 100;
  $: pctDay = (co2PerPerson / dayBudget) * 100;

  // Color logic: green below 100%, gradient above 100% (based on meal percentage)
  function getThermometerColor(percentage: number) {
    const maxValue = 500; // 500% for meal budget
    if (percentage <= 100) {
      return "#5ED4A3"; // Green for values at or below budget
    } else {
      // Apply gradient similar to GradientHeading
      const ratio = Math.min((percentage - 100) / (maxValue - 100), 1);
      if (ratio <= 0.5) {
        // Transition from green to yellow
        const r = Math.round(94 + (247 - 94) * (ratio * 2));
        const g = Math.round(212 + (215 - 212) * (ratio * 2));
        const b = Math.round(163 + (134 - 163) * (ratio * 2));
        return `rgb(${r}, ${g}, ${b})`;
      } else {
        // Transition from yellow to red
        const r = Math.round(251 + (247 - 251) * ((ratio - 0.5) * 2));
        const g = Math.round(215 + (121 - 215) * ((ratio - 0.5) * 2));
        const b = Math.round(134 + (125 - 134) * ((ratio - 0.5) * 2));
        return `rgb(${r}, ${g}, ${b})`;
      }
    }
  }

  $: thermometerColor = getThermometerColor(pctMeal);

  let showModal = false;
</script>

<Card class={cardClass}>
  <!-- Info icon in the top-right corner -->
  <button
    class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 focus:outline-none"
    on:click={() => (showModal = true)}
    aria-label="Vis budget detaljer"
  >
    <InfoCircleOutline class="w-5 h-5" />
  </button>

  <!-- Main content container with consistent height -->
  <div class="flex flex-col h-full min-h-0 lg:min-h-52">
    <!-- Centered container for budget comparisons -->
    <div class="flex-grow flex items-center justify-center">
      <div
        class="flex justify-center items-start gap-8 w-full max-w-md mx-auto"
      >
        <div class="flex flex-row items-start gap-2">
          <div class="flex flex-col items-center justify-center">
            <span class="text-3xl font-bold text-[#404040]"
              >{pctMeal.toFixed(0)}%</span
            >
            <span
              class="text-base sm:text-sm mt-2 sm:mt-1 text-[#404040] text-center"
              >af dit CO2e-budget per måltid</span
            >
          </div>
          <div class="flex items-start">
            <ThermometerChart
              value={pctMeal}
              budget={mealBudget}
              label="måltid"
              color={thermometerColor}
            />
          </div>
        </div>
        <div class="flex flex-row items-start gap-2">
          <div class="flex flex-col items-center">
            <span class="text-3xl font-bold text-[#404040]"
              >{pctDay.toFixed(0)}%</span
            >
            <span
              class="text-base sm:text-sm mt-2 sm:mt-1 text-[#404040] text-center"
              >af dit daglige måltids CO2e-budget</span
            >
          </div>
          <div class="flex items-start">
            <ThermometerChart
              value={pctDay}
              budget={dayBudget}
              label="dag"
              color={thermometerColor}
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Average person comparison -->
    <div class="flex flex-col items-center mt-12">
      <p class="text-sm text-center">
        Gennemsnitsdansker udleder {avgMeal} CO2e per måltid
      </p>
    </div>
  </div>
</Card>

<!-- Modal with budget details -->
<Modal bind:open={showModal}>
  <div slot="header">
    <h3 class="text-xl font-semibold">Budget Detaljer</h3>
  </div>
  <div class="p-6 space-y-4">
    <p>
      CO2e budgetter er baseret på Concito's rapport der estimere hvad en
      klima-venligt måltid udleder
      <a
        href="https://concito.dk/en/concito-bloggen/her-faar-du-mest-ernaering-klimaaftrykket-0?utm_source=chatgpt.com"
        target="_blank"
        rel="noopener noreferrer"
        class="text-blue-600 hover:text-blue-800 underline"
      >
        (læs mere her)
      </a>
    </p>
    <p>
      <span class="font-semibold">Måltid budget:</span>
      Budget på hvad der er et miljøvenligt måltid målt på CO2e på {mealBudget}
      kg CO2
    </p>
    <p>
      <span class="font-semibold">Dagligt budget:</span>
      Budget på hvad man må udlede på en dag fra fødevare på {dayBudget} kg CO2
    </p>
  </div>
  <div slot="footer" class="flex justify-end">
    <Button on:click={() => (showModal = false)}>Luk</Button>
  </div>
</Modal>
