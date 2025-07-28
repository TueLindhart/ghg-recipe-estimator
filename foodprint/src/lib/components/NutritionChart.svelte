<script lang="ts">
  import { Chart } from "flowbite-svelte";

  export let fat: number | null = null;
  export let carbohydrate: number | null = null;
  export let protein: number | null = null;

  // Calculate the total to set y-axis max exactly to the data range
  $: totalValue = (fat ?? 0) + (carbohydrate ?? 0) + (protein ?? 0);

  $: series = [
    {
      name: "Fedt",
      data: [fat ?? 0],
      color: "#EF4444",
    },
    {
      name: "Kulhydrat",
      data: [carbohydrate ?? 0],
      color: "#3B82F6",
    },
    {
      name: "Protein",
      data: [protein ?? 0],
      color: "#10B981",
    },
  ];

  $: options = {
    chart: {
      type: "bar" as const,
      height: "192px",
      width: "50%",
      toolbar: { show: false },
      offsetY: 0,
      offsetX: 0,
      margin: {
        top: 0,
        right: 0,
        bottom: 0,
        left: 0,
      },
      stacked: true,
      animations: {
        enabled: false,
      },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "90%",
        borderRadius: 4,
      },
    },
    dataLabels: {
      enabled: true,
      formatter: function (val: number, opts: any) {
        const seriesName = opts.w.config.series[opts.seriesIndex].name;
        return val > 0 ? `${seriesName}\n ${val}g` : "";
      },
      style: {
        fontSize: "10px",
        colors: ["#fff"],
        fontWeight: "bold",
      },
      textAnchor: "middle" as const,
    },
    series,
    xaxis: {
      categories: [""],
      labels: {
        show: false,
      },
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    yaxis: {
      show: false,
      min: 0,
      max: totalValue > 0 ? totalValue : 100,
      forceNiceScale: false,
      tickAmount: undefined,
    },
    grid: {
      show: false,
      padding: {
        top: 0,
        right: 0,
        bottom: 0,
        left: 0,
      },
    },
    legend: {
      show: false,
    },
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function (val: number) {
          return val + " g";
        },
      },
    },
  };
</script>

<div class="w-full h-fit flex justify-center">
  <Chart {options} />
</div>
