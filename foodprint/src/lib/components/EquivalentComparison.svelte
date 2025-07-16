<script lang="ts">
  import { Card } from "flowbite-svelte";

  export let co2PerPerson: number;
  export let cardClass = "max-w-full p-4 space-y-2";

  const CAR_KG_PER_KM = 0.19;
  const FLIGHT_KG_CPH_LON = 150;
  const WASH_KG_PER_HOUR = 0.6;

  $: km = co2PerPerson / CAR_KG_PER_KM;
  $: mealsForFlight = FLIGHT_KG_CPH_LON / co2PerPerson;
  $: washingHours = co2PerPerson / WASH_KG_PER_HOUR;
</script>

<Card class={cardClass}>
  <div>
    <span class="text-2xl font-bold">{km.toFixed(0)} km</span>
    <span class="text-sm"> i en benzinbil</span>
  </div>
  <div>
    <span class="text-2xl font-bold">{mealsForFlight.toFixed(0)}×</span>
    <span class="text-sm"> så mange måltider for en flyrejse KBH-London</span>
  </div>
  <div>
    <span class="text-2xl font-bold">{washingHours.toFixed(0)} timer</span>
    <span class="text-sm"> vaskemaskine</span>
  </div>
</Card>
