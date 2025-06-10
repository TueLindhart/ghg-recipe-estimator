<script lang="ts">
  import { goto } from "$app/navigation";
  import GradientHeading from "$lib/components/GradientHeading.svelte";
  import ProgressTimeline from "$lib/components/ProgressTimeline.svelte";
  import ReturnHomeButton from "$lib/components/ReturnHomeButton.svelte";
  // Flowbite-Svelte
  import { Alert } from "flowbite-svelte";

  import { onMount } from "svelte";

  // jobId arrives from load()
  export let data: { jobId: string };
  const { jobId } = data;

  let status: string = "Processing";
  let statusMessage = "";

  async function poll(): Promise<void> {
    try {
      const r = await fetch(`/api/status/${jobId}`);
      if (!r.ok) {
        let detail = `Fejl ved statusopdatering: ${r.status}`;
        try {
          const errorBody = await r.json();
          if (errorBody?.error) {
            detail = `Fejl ved statusopdatering: ${errorBody.error}`;
          }
        } catch {
          // fallback to status if response is not JSON
        }
        statusMessage = detail;
        return;
      }

      const resp = (await r.json()) as { status: string; result?: string };
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
  <title>MyFoodPrint - calculating</title>
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
