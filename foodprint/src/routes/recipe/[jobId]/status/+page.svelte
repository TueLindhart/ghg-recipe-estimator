<script lang="ts">
  import { goto, invalidate } from "$app/navigation";
  import { page } from "$app/stores";
  import { get } from "svelte/store";
  import GradientHeading from "$lib/components/GradientHeading.svelte";
  import ProgressTimeline from "$lib/components/ProgressTimeline.svelte";
  import ReturnHomeButton from "$lib/components/ReturnHomeButton.svelte";
  // Flowbite-Svelte
  import { Alert } from "flowbite-svelte";

  import { onMount } from "svelte";

  // jobId and initial status arrive from load()
  export let data: { jobId: string; status: string; result?: string };
  const { jobId } = data;

  let status: string = data.status;
  let statusMessage = "";

  async function poll(): Promise<void> {
    try {
      await invalidate(`/recipe/${jobId}/status`);
      const resp = get(page).data as {
        jobId: string;
        status: string;
        result?: string;
      };
      status = resp.status;

      if (status === "Completed") {
        setTimeout(() => goto(`/recipe/${jobId}/estimate`), 1_000);
      } else if (status === "Error") {
        statusMessage = `Fejl: ${resp.result}`;
      } else {
        setTimeout(poll, 2_000);
      }
    } catch (e) {
      statusMessage = "Ups! Noget gik galt. Prøv igen.";
      console.error("Error fetching status:", e);
    }
  }

  onMount(poll);
</script>

<svelte:head>
  <title>MyFoodprint - calculating</title>
</svelte:head>

<div
  class="container mx-auto px-4 py-8 flex flex-col items-center justify-center min-h-screen"
>
  <GradientHeading
    tag="h2"
    text="Der arbejdes på din opskrift..."
    className="mb-8 text-center"
  />

  <ProgressTimeline {status} />

  {#if statusMessage}
    <!-- Flowbite alert with button -->
    <Alert
      color="red"
      rounded
      withBorderAccent
      role="alert"
      class="mt-6 w-full max-w-md flex items-center gap-4"
    >
      <span class="flex-1">{statusMessage}</span>
      <ReturnHomeButton />
    </Alert>
  {/if}
</div>
