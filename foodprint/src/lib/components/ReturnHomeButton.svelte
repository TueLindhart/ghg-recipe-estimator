<script lang="ts">
  import { goto } from "$app/navigation";
  import { Button } from "flowbite-svelte";
  import { ArrowLeftOutline } from "flowbite-svelte-icons";

  /** Where to send the user. Defaults to the site root. */
  export let to: string = "/";

  /** Caption shown next to the icon (hidden on < sm). */
  export let label: string = "Hjem";

  /** Navigate without full reload (SvelteKit SPA). */
  const navigate = (): void => goto(to);
</script>

<Button
  class="flex items-center gap-1"
  aria-label={`Gå til ${label}`}
  on:click={navigate}
>
  <ArrowLeftOutline class="w-4 h-4" />
  <span class="hidden sm:inline">{label}</span>
</Button>
