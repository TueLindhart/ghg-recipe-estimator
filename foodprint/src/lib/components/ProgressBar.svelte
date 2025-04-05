<script>
    import { Progressbar } from 'flowbite-svelte';
    import { sineOut } from 'svelte/easing';
    export let indeterminate = true;
    export let color = "green";
    let progress = '100'

  </script>
  
  <Progressbar
  {progress}
  animate
  precision={2}
  labelOutside="With animation"
  labelInside
  tweenDuration={1500}
  easing={sineOut}
  size="h-6"
  class="mb-8"
/>