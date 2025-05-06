<script lang="ts">
  import { Heading as FlowbiteHeading } from "flowbite-svelte";

  /**
   * Semantic heading level ( `h1` … `h6` ).
   */
  export let tag: "h1" | "h2" | "h3" | "h4" | "h5" | "h6" = "h1";

  /**
   * Text the heading should display.
   */
  export let text: string;

  /**
   * Optional extra classes (spacing, alignment, size utilities, …).
   */
  export let className = "";
</script>

<FlowbiteHeading {tag} class={`font-bold leading-tight ${className}`}>
  <span
    class="inline-block text-transparent bg-clip-text bg-gradient-to-r from-[#f7797d] via-[#fbd786] to-[#5ED4A3]"
  >
    {text}
  </span>
</FlowbiteHeading>
