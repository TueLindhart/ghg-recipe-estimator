# Foodprint Frontend Learnings

## Project Structure & Focus
- GHG (CO2e) recipe estimator with Svelte frontend and Python backend
- Foodprint agent handles UI/UX for recipe CO2e calculations and visualizations
- Project follows consistent component patterns for maintainability and reusability

## UI/UX Architecture
- **Estimate Page Layout**: `OverviewCard` displays CO2e per person prominently with larger font
- **Tab Structure**: Three main tabs positioned above content (not beside): 
  - "Sammenlign" (Compare): Budget comparison with percentage displays
  - "Svare til" (Equivalent): Equivalency comparisons (car km, flights, appliances)
  - "Næringsindhold" (Nutrition): Energy and macronutrient information
- **Secondary Tabs**: Below main tabs for "Ingredienser" and "Graf" with metric selection

## Component Design System
- **Info Icon Pattern**: Consistent across all components
  - Card with `relative` class and `p-4` padding
  - Info button: `absolute top-2 right-2` positioning
  - Standard hover states and accessibility
- **Text Hierarchy**: 
  - Primary numbers: `text-2xl font-bold` or `text-3xl font-bold`
  - Labels: `text-sm mt-1`
  - Supporting text: `text-xs text-gray-600`
- **Spacing Standards**: 
  - Section spacing: `mb-4`
  - Element spacing: `gap-12`
  - Related elements: `mt-1`

## Layout Requirements
- **Vertical Stacking**: Use `flex flex-col` for main layout, not `lg:flex-row`
- **Responsive Design**: Cards should be compact on large screens, not full-width
- **Content Alignment**: Center alignment for metrics, left for descriptions
