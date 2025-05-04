<script lang="ts">
  import ProgressBar from "$lib/components/ProgressBar.svelte"; // YOUR component
  import { goto } from "$app/navigation";
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
        goto(`/recipe/${uid}/estimate`);
      } else if (status === "Error") {
        statusMessage = `Fejl: ${resp.result}`;
      } else {
        setTimeout(poll, 2000);
      }
    } catch (e) {
      statusMessage = `Fejl ved polling: ${(e as Error).message}`;
    }
  }

  onMount(poll);
</script>

<!-- Your component needs **only** the status prop -->
<ProgressBar {status} />

{#if statusMessage}
  <p class="text-lg text-red-600">{statusMessage}</p>
{/if}
