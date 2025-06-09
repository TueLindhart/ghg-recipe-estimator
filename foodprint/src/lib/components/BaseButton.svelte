<script lang="ts">
  import { Button } from "flowbite-svelte";

  /** Accessible label (always required). */
  export let ariaLabel!: string;

  /** Click handler. */
  export let onClick: () => void = () => {};
</script>

<!--
  h-10 gives a fixed 40 px height on every breakpoint.
  px-4 / gap-1 keep text & icon spacing consistent.
-->
<Button
  class="h-10 px-4 flex items-center gap-1"
  aria-label={ariaLabel}
  on:click={onClick}
>
  <!-- Consumers decide what goes inside (icon, text, both, …) -->
  <slot />
</Button>
