<script lang="ts">
  import "../app.css";

  import AppNavbar from "$lib/components/NavBar.svelte";
</script>

<!-- ─── PAGE-WIDE HEADER ──────────────────────────────── -->
<AppNavbar />

<!-- ─── ROUTE CONTENT ─────────────────────────────────── -->
<slot />
<!-- This is SvelteKit’s standard outlet for child pages -->
