<script lang="ts">
  import { Chart } from "flowbite-svelte";

  export let fat: number | null = null;
  export let carbohydrate: number | null = null;
  export let protein: number | null = null;

  $: series = [
    {
      name: "Gram",
      data: [fat ?? 0, carbohydrate ?? 0, protein ?? 0],
      color: "#404040"
    }
  ];

  $: options = {
    chart: {
      type: "bar",
      height: "200px",
      maxWidth: "100%",
      toolbar: { show: false },
      offsetY: 0,
      padding: { top: 0, bottom: 0 }
    },
    plotOptions: {
      bar: { horizontal: true, columnWidth: "70%", borderRadius: 4 }
    },
    dataLabels: { enabled: false },
    series,
    xaxis: {
      categories: ["Fedt", "Kulhydrat", "Protein"],
      title: { text: "Gram" },
      labels: { style: { fontFamily: "Inter, sans-serif" } }
    },
    yaxis: {
      labels: { style: { fontFamily: "Inter, sans-serif", fontSize: "12px" } }
    },
    tooltip: { shared: true, intersect: false }
  };
</script>

<div class="w-full">
  <Chart {options} />
</div>
