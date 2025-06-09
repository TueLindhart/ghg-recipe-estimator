<script lang="ts">
  import { Chart } from "flowbite-svelte";

  import type { IngredientOutput } from "$lib";

  export let ingredients: IngredientOutput[] = [];

  // Only keep positive emissions
  $: filtered = ingredients.filter((i) => i.co2_kg != null && i.co2_kg > 0);

  // Build the single series for the chart
  $: series = [
    {
      name: "CO₂e udledning (kg)",
      data: filtered.map((i) => i.co2_kg as number),
      color: "#404040",
    },
  ];

  // Categories are your ingredient names
  $: categories = filtered.map((i) => i.name);

  // Make options reactive so the chart updates whenever series or categories change
  $: options = {
    chart: {
      type: "bar",
      height: "300px", // visible height
      maxWidth: "100%", // fill container width
      toolbar: { show: false },
      offsetY: 0,
      padding: { top: 0, bottom: 0 },
    },
    plotOptions: {
      bar: {
        horizontal: true,
        columnWidth: "70%",
        borderRadius: 4,
      },
    },
    dataLabels: { enabled: false },
    series, // reactive series
    xaxis: {
      categories,
      title: { text: "CO₂ udledning (kg)" },
      labels: {
        style: { fontFamily: "Inter, sans-serif" },
      },
    },
    yaxis: {
      labels: {
        style: { fontFamily: "Inter, sans-serif", fontSize: "12px" },
      },
    },
    tooltip: { shared: true, intersect: false },
  };
</script>

<div class="w-full">
  <Chart {options} />
</div>
