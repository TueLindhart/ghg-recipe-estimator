<script lang="ts">
  import { Card } from "flowbite-svelte";
  import { onMount } from "svelte";

  /* ───────── Props ───────── */
  export let ratio: number;         // 0 – ∞  (1 = 100 %)
  export let helperText: string;

  /* ───────── Derived values ───────── */
  $: ratioPercent = ratio * 100;
  $: carPos = Math.min(ratioPercent, 100);        // clamp 0-100 %

  $: strokeClass =
    ratioPercent < 50
      ? "stroke-green-500"
      : ratioPercent < 100
      ? "stroke-yellow-400"
      : "stroke-red-600";

  /* ───────── Path maths ───────── */
  let pathEl: SVGPathElement;
  let carX = 0, carY = 0;

  function updateCarCoords() {
    if (!pathEl) return;
    const len = pathEl.getTotalLength();
    const pt  = pathEl.getPointAtLength((carPos / 100) * len);
    carX = pt.x;
    carY = pt.y;
  }

  onMount(updateCarCoords);
  $: updateCarCoords();   // run whenever carPos changes
</script>

<Card class="!max-w-none w-full md:w-1/2 bg-white border border-gray-200 rounded-lg shadow">
  <div class="flex flex-col items-center gap-4 p-6">   <!-- ↓ tighter gap -->

    <!-- ───── Curved road ───── -->
    <div class="relative w-full max-w-md h-20">        <!-- ↓ shorter height -->
      <!-- City codes anchored at ends -->
      <span class="absolute left-0 -top-1 text-sm font-medium uppercase text-gray-600 select-none">
        KBH
      </span>
      <span class="absolute right-0 -top-1 text-sm font-medium uppercase text-gray-600 select-none">
        AAL
      </span>

      <!-- SVG arc -->
      <svg viewBox="0 0 300 80" class="w-full h-full select-none">
        <!-- grey background -->
        <path d="M 0 60 Q 150 0 300 60" stroke="#E5E7EB" stroke-width="4" fill="none" />

        <!-- coloured progress -->
        <path
          bind:this={pathEl}
          d="M 0 60 Q 150 0 300 60"
          class={strokeClass}
          stroke-width="4"
          fill="none"
          stroke-dasharray="300"
          style="stroke-dashoffset:{300 - carPos * 3}"
        />

        <!-- car -->
        <text
          x={carX}
          y={carY}
          dy="-2"
          text-anchor="middle"
          font-size="20"
          aria-label="Car position"
        >🚘</text>
      </svg>
    </div>

    <!-- Percentage -->
    <div class="text-center">
      <span class="text-2xl md:text-3xl font-extrabold tracking-tight text-gray-900">
        {ratioPercent.toFixed(2)}%
      </span>
    </div>

    <!-- Helper text -->
    <p class="text-center text-sm text-gray-700">{helperText}</p>
  </div>
</Card>