<script lang="ts">
  import { goto } from "$app/navigation";
  import GradientHeading from "$lib/components/GradientHeading.svelte";
  import ProgressTimeline from "$lib/components/ProgressTimeline.svelte";
  import { onMount } from "svelte";

  // uid arrives from load()
  export let data: { uid: string };
  const { uid } = data;

  let status: string = "Processing";
  let statusMessage = "";

  async function poll(): Promise<void> {
    try {
      const r = await fetch(`/api/status/${uid}`);
      if (!r.ok) {
        statusMessage = `Fejl ved statusopdatering: ${r.statusText}`;
        return;
      }
      const resp = (await r.json()) as { status: string; result?: string };
      status = resp.status;

      if (status === "Completed") {
        setTimeout(() => {
          goto(`/recipe/${uid}/result`);
        }, 1000);
      } else if (status === "Error") {
        statusMessage = `Fejl: ${resp.result}`;
      } else {
        setTimeout(poll, 2000);
      }
    } catch (e) {
      statusMessage = `Ups! Noget gik galt. Prpøv igen.`;
      console.error("Error fetching status:", e);
    }
  }

  onMount(poll);
</script>

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
    <p class="text-lg text-red-600 mt-4 text-center">{statusMessage}</p>
  {/if}
</div>
