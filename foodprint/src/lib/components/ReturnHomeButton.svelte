<script lang="ts">
  import { goto } from "$app/navigation";
  import BaseButton from "$lib/components/BaseButton.svelte";
  import { ArrowLeftOutline } from "flowbite-svelte-icons";

  export let to: string = "/";
  export let label: string = "Tilbage";

  const navigate = (): void => goto(to);
</script>

<BaseButton ariaLabel={`Gå til ${label}`} onClick={navigate}>
  <ArrowLeftOutline class="w-4 h-4" />
  <!-- Hide text below the sm breakpoint, but height stays 40 px -->
  <span class="hidden sm:inline">{label}</span>
</BaseButton>
