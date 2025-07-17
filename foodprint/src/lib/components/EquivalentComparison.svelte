<script lang="ts">
  import type { Comparison } from "$lib/types";
  import { Card } from "flowbite-svelte";
  import { Car, Plane, WashingMachine } from "lucide-svelte";

  export let comparisons: Comparison[];
  export let cardClass = "";

  // Function to get the appropriate icon based on the comparison label
  function getIcon(label: string) {
    if (label.includes("Dieselbil")) {
      return Car;
    } else if (label.includes("Flyrejse")) {
      return Plane;
    } else if (label.includes("Vaskemaskine")) {
      return WashingMachine;
    }
    return Car; // Default fallback
  }
</script>

<Card class={cardClass}>
  <!-- Centered container for equivalent comparisons -->
  <div class="flex-grow flex items-start lg:items-center justify-center">
    <div class="flex justify-center items-start lg:items-center gap-12">
      {#each comparisons as comparison}
        <div class="flex flex-col items-center">
          <!-- Icon -->
          <svelte:component
            this={getIcon(comparison.label)}
            class="w-8 h-8 text-[#404040] mb-3"
          />
          <!-- Number -->
          <span class="text-3xl font-bold text-[#404040]"
            >{comparison.comparison.toFixed(0)}</span
          >
          <!-- Description -->
          <span class="text-sm mt-1 text-[#404040] text-center"
            >{comparison.help_text}</span
          >
        </div>
      {/each}
    </div>
  </div>
</Card>
