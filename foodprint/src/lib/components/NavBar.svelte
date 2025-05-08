<script lang="ts">
  import { Navbar, NavBrand } from "flowbite-svelte";

  /**
   * The root link of the brand text (override from parent if needed).
   */
  export let href: string = "/";
</script>

<!-- Header without intrinsic bottom border -->
<Navbar>
  <NavBrand {href}>
    <span
      class="self-center whitespace-nowrap text-2xl md:text-3xl font-semibold text-[#404040]"
    >
      MyFoodprint
    </span>
  </NavBrand>
</Navbar>
<!-- Gradient line separator -->
<div
  class="w-full h-px bg-gradient-to-r from-[#f7797d] via-[#fbd786] to-[#5ED4A3]"
></div>
