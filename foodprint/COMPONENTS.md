# Component Architecture

## Core Components

### Page Layout Components
1. `+page.svelte`
   - Main container with responsive padding
   - Header section with title and navigation
   - Overview and tabs section
   - Content sections with ingredient grid and charts

### Reusable UI Components
1. `BaseButton.svelte`
   - Standard button component
   - Used for primary actions

2. `IngredientCard.svelte`
   - Display component for ingredient information
   - Shows emissions, weight, and nutritional data
   - Info button for detailed notes
   - Consistent text styling and spacing

3. `OverviewCard.svelte`
   - Summary card for recipe data
   - Used in main estimate page

4. `EmissionBarChart.svelte`
   - Visualization component
   - Supports multiple metrics (CO2e, energy, nutrients)

5. `NutritionChart.svelte`
   - Displays nutritional information
   - Used in nutrition tab

### Data Display Patterns
1. Measurements
   - CO2e values shown in kg
   - Energy in kJ
   - Nutrients in g
   - Always show units
   - Use fallback value of 0 when data is null

2. Modal Patterns
   - Used for detailed information
   - Consistent header, body, footer structure
   - Close button in footer
   - Pre-formatted text for notes

## Component Communication
1. Props
   - Use TypeScript types for prop definitions
   - Default values for optional props
   - Null coalescing for safety (`?? 0`)

2. Events
   - Custom event handlers (e.g., `onShowNotes`)
   - Consistent naming pattern

## Layout Structure
1. Container Layout
```svelte
<div class="container mx-auto px-4">
  <!-- Page content -->
</div>
```

2. Section Layout
```svelte
<div class="mb-8 flex flex-col lg:flex-row gap-6">
  <!-- Section content -->
</div>
```

3. Tab Layout
```svelte
<Tabs tabStyle="pill">
  <TabItem title="Title">
    <!-- Tab content -->
  </TabItem>
</Tabs>
```

## Best Practices
1. Use TypeScript for type safety
2. Implement responsive designs
3. Keep components focused and single-purpose
4. Use consistent prop and event naming
5. Maintain accessibility standards
6. Document component interfaces
