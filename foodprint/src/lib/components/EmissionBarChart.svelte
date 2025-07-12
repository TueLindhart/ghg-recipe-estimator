<script lang="ts">
  import { Chart } from "flowbite-svelte";

  import type { IngredientOutput } from "$lib";

  export let ingredients: IngredientOutput[] = [];
  export let metric: "co2" | "energy" | "protein" | "carbohydrate" | "fat" = "co2";

  // Filter out entries without the chosen metric
  $: filtered = ingredients.filter((i) => {
    switch (metric) {
      case "energy":
        return i.energy_kj != null && i.energy_kj > 0;
      case "protein":
        return i.protein_g != null && i.protein_g > 0;
      case "carbohydrate":
        return i.carbohydrate_g != null && i.carbohydrate_g > 0;
      case "fat":
        return i.fat_g != null && i.fat_g > 0;
      default:
        return i.co2_kg != null && i.co2_kg > 0;
    }
  });

  // Build the single series for the chart
  $: yField = metric === "energy"
      ? "energy_kj"
      : metric === "protein"
      ? "protein_g"
      : metric === "carbohydrate"
      ? "carbohydrate_g"
      : metric === "fat"
      ? "fat_g"
      : "co2_kg";

  $: unitLabel = metric === "energy"
      ? "kJ"
      : metric === "protein" || metric === "carbohydrate" || metric === "fat"
      ? "g"
      : "kg";

  $: series = [
    {
      name:
        metric === "energy"
          ? "Energi"
          : metric === "protein"
          ? "Protein"
          : metric === "carbohydrate"
          ? "Kulhydrat"
          : metric === "fat"
          ? "Fedt"
          : "CO₂e udledning",
      data: filtered.map((i) => (i[yField] as number)),
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
      title: { text: `${series[0].name} (${unitLabel})` },
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
