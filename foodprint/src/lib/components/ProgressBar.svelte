<script>
  import { Progressbar } from "flowbite-svelte";
  import { sineOut } from "svelte/easing";

  export let status = "";

  const statusProgress = {
    Text: 20,
    Recipe: 40,
    Weights: 60,
    RAGCO2: 80,
    Preparing: 90,
    Completed: 100,
    Processing: 50,
    Error: 0,
  };

  const statusMessages = {
    Text: "Henter opskrift fra URL...",
    Recipe: "Udtrækker ingredienser...",
    Weights: "Estimerer vægt per ingrediens...",
    RAGCO2: "Estimerer CO2 udledning per ingrediens...",
    Preparing: "Forbereder resultater...",
    Processing: "Behandler opskrift...",
    Completed: "Færdig!",
    Error: "Fejl",
  };

  $: progress = statusProgress[status] || 0;
  $: statusMessage = statusMessages[status] || "";
</script>

<Progressbar
  {progress}
  animate
  precision={2}
  labelOutside={statusMessage}
  labelInside
  tweenDuration={1500}
  easing={sineOut}
  size="h-6"
  class="mb-8"
/>
