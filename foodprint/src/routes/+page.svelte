<script lang="ts">
  import { goto } from "$app/navigation";
  import InputBar from "$lib/components/InputBar.svelte";

  let recipeUrl = "";
  let statusMessage = "";

  // Beholder den oprindelige funktion til at opdatere recipeUrl
  const handleInputChange = (val: string) => {
    recipeUrl = val;
  };

  async function startEstimation(): Promise<void> {
    statusMessage = ""; // Nulstil status
    if (!recipeUrl) {
      statusMessage = "Angiv venligst en URL.";
      return;
    }

    try {
      const r = await fetch("/api/estimate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: recipeUrl }),
      });

      if (!r.ok) {
        const errorData = await r
          .json()
          .catch(() => ({ message: r.statusText }));
        statusMessage = `Fejl ved start af estimering (${r.status}): ${errorData.message || r.statusText}`;
        return;
      }

      const { uid } = (await r.json()) as { uid: string };

      goto(`/recipe/${uid}/progress`);
    } catch (err) {
      console.error("Fetch error:", err);
      statusMessage = `Netværksfejl eller server utilgængelig: ${(err as Error).message}`;
    }
  }
</script>

<div class="flex justify-center items-center min-h-screen px-4">
  <div class="w-full">
    <InputBar
      {recipeUrl}
      onInputChange={handleInputChange}
      onButtonClick={startEstimation}
    />

    {#if statusMessage}
      <p class="mt-4 text-center text-lg text-red-600">{statusMessage}</p>
    {/if}
  </div>
</div>
