<script lang="ts">
  import { Card, Timeline, TimelineItem } from "flowbite-svelte";
  import {
    CheckCircleSolid,
    CircleMinusSolid,
    ClockSolid,
  } from "flowbite-svelte-icons";
  import type { SvelteComponent } from "svelte";

  export let status: string = "";

  type StepStatus = "completed" | "in-progress" | "not-started";

  interface Step {
    id: string;
    text: string;
  }

  const steps: Step[] = [
    { id: "Text", text: "Henter opskrift fra URL" },
    { id: "Recipe", text: "Udtrækker ingredienser" },
    { id: "Weights", text: "Estimerer vægt per ingrediens" },
    { id: "RAGCO2", text: "Estimerer CO2 udledning per ingrediens" },
    { id: "Preparing", text: "Forbereder resultater" },
  ];

  const statusOrder: string[] = [
    "Text",
    "Recipe",
    "Weights",
    "RAGCO2",
    "Preparing",
  ];

  function getStepStatus(stepId: string): StepStatus {
    if (status === "Processing") {
      return stepId === "Text" ? "in-progress" : "not-started";
    }
    if (status === "Error") {
      return "not-started";
    }
    if (status === "Completed") {
      return "completed";
    }

    const currentIndex: number = statusOrder.indexOf(status);
    const stepIndex: number = statusOrder.indexOf(stepId);

    if (currentIndex === -1 || stepIndex === -1) {
      return "not-started";
    }

    if (stepIndex < currentIndex) {
      return "completed";
    }
    if (stepIndex === currentIndex) {
      return "in-progress";
    }
    return "not-started";
  }

  function getStatusAttributes(stepStatus: StepStatus): {
    icon: typeof SvelteComponent;
    colorClass: string;
  } {
    switch (stepStatus) {
      case "completed":
        return { icon: CheckCircleSolid, colorClass: "text-green-500" };
      case "in-progress":
        return { icon: ClockSolid, colorClass: "text-blue-500" };
      case "not-started":
      default:
        return { icon: CircleMinusSolid, colorClass: "text-gray-500" };
    }
  }
</script>

<Card class="mb-8">
  <Timeline order="vertical">
    {#each steps as step (step.id)}
      {@const stepStatus = getStepStatus(step.id)}
      {@const attrs = getStatusAttributes(stepStatus)}

      <!-- ↓ add classLi="last:mb-0" -->
      <TimelineItem title={step.text} classLi="last:mb-0">
        <svelte:fragment slot="icon">
          <span
            class="flex absolute -start-3 justify-center items-center
							   w-6 h-6 rounded-full ring-8 ring-white"
          >
            <svelte:component
              this={attrs.icon}
              class="w-4 h-4 {attrs.colorClass}"
            />
          </span>
        </svelte:fragment>
      </TimelineItem>
    {/each}

    {#if status === "Error"}
      <TimelineItem title="Fejl opstået" classLi="last:mb-0">
        <svelte:fragment slot="icon">
          <span
            class="flex absolute -start-3 justify-center items-center
							   w-6 h-6 rounded-full ring-8 ring-white"
          >
            <CircleMinusSolid class="w-4 h-4 text-red-500" />
          </span>
        </svelte:fragment>
      </TimelineItem>
    {/if}
  </Timeline>
</Card>
