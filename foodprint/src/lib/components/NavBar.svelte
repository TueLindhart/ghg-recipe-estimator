<script lang="ts">
  import { Navbar, NavBrand } from "flowbite-svelte";

  /**
   * The root link of the brand text (override from parent if needed).
   */
  export let href: string = "/";
</script>

<!-- Header with a subtle bottom border to separate it from the body -->
<Navbar class="border-b border-gray-200 dark:border-gray-700">
  <NavBrand {href}>
    <span
      class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
    >
      Foodprint
    </span>
  </NavBrand>
</Navbar>
