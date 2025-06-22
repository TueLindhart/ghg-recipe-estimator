<script lang="ts">
  import { goto } from "$app/navigation";
  import GradientHeading from "$lib/components/GradientHeading.svelte";
  import InputBar from "$lib/components/InputBar.svelte";
  import { P } from "flowbite-svelte";

  let recipeUrl = "";
  let statusMessage = "";
  let isLoading = false;

  // Beholder den oprindelige funktion til at opdatere recipeUrl
  const handleInputChange = (val: string) => {
    recipeUrl = val;
  };

  async function startEstimation(): Promise<void> {
    if (isLoading) return;

    statusMessage = ""; // Nulstil status
    if (!recipeUrl) {
      statusMessage = "Angiv venligst en URL.";
      return;
    }

    isLoading = true;
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

      const { uid: jobId } = (await r.json()) as { uid: string };
      goto(`/recipe/${jobId}/status`);
    } catch (err) {
      console.error("Fetch error:", err);
      statusMessage = `Ups! Noget gik galt. Prøv igen senere.`;
    } finally {
      isLoading = false;
    }
  }
</script>

<svelte:head>
  <title>MyFoodprint</title>
</svelte:head>

<div class="flex justify-center items-start min-h-screen px-4 pt-[15vh]">
  <div class="w-full">
    <GradientHeading
      tag="h1"
      text="Forstå udledningen fra dit måltid."
      className="mb-8 text-center"
    />
    <P class="mb-4 text-center text-xl">
      Indtast URL for at starte estimeringen af CO2-udledningen fra din
      opskrift.
    </P>
    <InputBar
      {recipeUrl}
      onInputChange={handleInputChange}
      onButtonClick={startEstimation}
      disabled={isLoading}
    />

    {#if statusMessage}
      <p class="mt-4 text-center text-lg text-red-600">{statusMessage}</p>
    {/if}
  </div>
</div>
