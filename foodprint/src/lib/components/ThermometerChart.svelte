<script lang="ts">
  export let value: number; // Current percentage value
  export let budget: number; // Budget value for labels
  export let label: string; // Chart label

  // Calculate max value (5x budget for meal, 2x budget for day)
  $: maxValue = label.includes('måltid') ? 500 : 200; // 500% for meal, 200% for day
  
  // Color logic: green below 100%, gradient above 100%
  function getColor(percentage: number) {
    if (percentage <= 100) {
      return '#5ED4A3'; // Green for values at or below budget
    } else {
      // Apply gradient similar to GradientHeading
      const ratio = Math.min((percentage - 100) / (maxValue - 100), 1);
      if (ratio <= 0.5) {
        // Transition from green to yellow
        const r = Math.round(94 + (247 - 94) * (ratio * 2));
        const g = Math.round(212 + (215 - 212) * (ratio * 2));
        const b = Math.round(163 + (134 - 163) * (ratio * 2));
        return `rgb(${r}, ${g}, ${b})`;
      } else {
        // Transition from yellow to red
        const r = Math.round(251 + (247 - 251) * ((ratio - 0.5) * 2));
        const g = Math.round(215 + (121 - 215) * ((ratio - 0.5) * 2));
        const b = Math.round(134 + (125 - 134) * ((ratio - 0.5) * 2));
        return `rgb(${r}, ${g}, ${b})`;
      }
    }
  }

  // Calculate the height percentage for the bar
  $: barHeight = Math.min((value / maxValue) * 100, 100);
  $: barColor = getColor(value);
  $: actualValue = (value * budget / 100).toFixed(1);
</script>

<div class="relative w-12 h-32">
  <!-- Thermometer container with grey background -->
  <div class="relative w-8 h-32 bg-gray-200 rounded-md overflow-hidden">
    <!-- The actual thermometer bar that fills from bottom -->
    <div 
      class="absolute bottom-0 left-0 w-full rounded-md transition-all duration-300 ease-out"
      style="height: {barHeight}%; background-color: {barColor};"
      title="{actualValue} kg CO2e"
    ></div>
  </div>
  
  <!-- Budget indicator line and label -->
  <div class="absolute top-0 left-0 w-full h-full pointer-events-none">
    <!-- 100% budget line -->
    <div 
      class="absolute w-8 border-t-2 border-gray-600"
      style="bottom: {(100 / maxValue) * 100}%"
    >
      <!-- Budget value label (positioned to the right) -->
      <div class="absolute left-10 -top-2 text-xs font-medium text-gray-600">
        {budget}
      </div>
    </div>
  </div>
  
  <!-- Unit label below the thermometer -->
  <div class="w-8 text-center mt-1">
    <div class="text-xs text-gray-500">kg CO2e</div>
  </div>
</div>
