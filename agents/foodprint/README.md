# Frontend (`foodprint`)

The `foodprint` directory contains the SvelteKit-based user interface for the CO₂ recipe estimator. It provides a modern, responsive web application that communicates with the FastAPI backend and displays comprehensive recipe emission analysis with real-time progress tracking.

## Project Context & Purpose
- **GHG Recipe Estimator**: Web application for calculating CO₂ emissions from recipes
- **User Experience Focus**: Clean, intuitive interface for environmental impact awareness
- **Real-time Processing**: Live progress updates during recipe analysis
- **Educational Component**: Comparison data to help users understand emission context

## Architecture & Structure

### Core Directories
- **`src/routes`**: API routes and pages
  - `api/estimate/+server.ts`: Proxies POST requests to backend `/estimate` endpoint
  - `api/status/+server.ts`: Handles job status polling
  - `api/comparison/+server.ts`: Fetches comparison data for visualizations
  - `estimate/+page.svelte`: Main estimation page with redesigned layout
- **`src/lib`**: Reusable components and TypeScript types
  - `components/`: Custom Svelte components for the redesign project
  - `types.ts`: TypeScript interfaces matching backend response models
- **`static`**: Static assets including icons and images
- **Configuration**: `svelte.config.js`, `vite.config.ts`, `package.json`

### Technology Stack
- **SvelteKit**: Modern web framework with SSR and routing
- **TypeScript**: Type safety and developer experience
- **Tailwind CSS**: Utility-first styling framework
- **Flowbite Svelte**: Component library built on Tailwind
- **Vite**: Fast build tool and development server

## Redesign Project Implementation

### Main Estimate Page Layout
The estimate page (`src/routes/estimate/+page.svelte`) implements a responsive layout with:
- **Overview Card**: Prominent display of CO₂ per person
- **Information Tabs**: Three main tabs for different data views
- **Secondary Navigation**: Ingredient and chart tabs within main tabs

### Custom Components (redesign-estimate-page)

#### Core Display Components
- **`OverviewCard.svelte`**: Primary CO₂ emission display with large, centered numbers
- **`BudgetComparison.svelte`**: Percentage comparisons against meal/daily CO₂ budgets
- **`EquivalentComparison.svelte`**: Real-world equivalencies (car km, flights, appliances)
- **`NutritionChart.svelte`**: Energy and macronutrient visualization

#### Supporting Components
- **`EmissionBarChart.svelte`**: Configurable chart for different metrics
- **`IngredientCard.svelte`**: Individual ingredient emission details
- **Status tracking components**: Real-time progress indicators

### Component Design System

#### Established Patterns
- **Info Icon Pattern**: Consistent top-right positioning with modal details
- **Text Hierarchy**: Large numbers (`text-3xl font-bold`), smaller labels (`text-sm mt-1`)
- **Card Layout**: Relative positioning with flexible height via `cardClass` prop
- **Responsive Design**: Mobile-first with desktop enhancements

#### Layout Standards
- **Vertical Stacking**: `flex flex-col` for main layout structure
- **Spacing**: Consistent gap patterns (`gap-6`, `gap-12`)
- **Height Management**: `min-h-80` for tab content, `py-12` for padding
- **Component Flexibility**: All styling customizable via props

## User Experience & Design Principles

### Visual Hierarchy (User Validated)
- **Primary Numbers**: Must be visually dominant and centered
- **Supporting Text**: Clearly secondary but readable
- **Proportional Sizing**: Significant size difference between primary and secondary elements
- **Compact Layout**: Cards should be 1/3 to 1/2 screen width on desktop

### User Preferences (from Design Process)
- **Iterative Feedback**: User prefers to see changes and provide incremental feedback
- **Visual Confirmation**: Screenshots and live previews essential for design decisions
- **Quick Adjustments**: Frequent small styling changes (fonts, spacing)
- **Clear Organization**: Information should be logically grouped in tabs

### Information Architecture
- **Three Main Tabs**: 
  - "Sammenlign" (Compare): Budget percentages and context
  - "Svare til" (Equivalent): Real-world comparison equivalents
  - "Næringsindhold" (Nutrition): Energy and macronutrient data
- **Secondary Navigation**: Ingredient details and chart options
- **Modal Details**: Additional information accessible via info icons

## Technical Implementation Details

### Flowbite Svelte Integration
- **Tabs Component**: `tabStyle="underline"` for clean professional appearance
- **Card Component**: Base styling with flexible customization via props
- **Chart Component**: ApexCharts integration for data visualization
- **Modal Component**: Consistent structure for additional information

### State Management
- **Reactive Statements**: `$:` for automatic updates when data changes
- **Props Pattern**: Clear separation between layout and content customization
- **Type Safety**: Full TypeScript interfaces for all data structures

### API Integration
- **Job Management**: Polling pattern for long-running estimation tasks
- **Error Handling**: Graceful degradation and user-friendly error messages
- **Real-time Updates**: Status polling for progress indication
- **Comparison Data**: Separate endpoint for visualization data

## Development Context & Standards

### Coding Standards (aligned with project RULES.md)
- **Type Hints**: Comprehensive TypeScript usage
- **SOLID Principles**: Component separation and single responsibility
- **Readability**: Clear, maintainable code structure
- **Consistency**: Established patterns followed across components

### Styling Philosophy
- **Component Modularity**: Each component handles its own core styling
- **Prop-based Customization**: Layout and sizing controlled via props
- **Design System**: Consistent patterns for repeated elements
- **Responsive Design**: Mobile-first with progressive enhancement

### Performance Considerations
- **Component Loading**: Efficient imports and lazy loading where appropriate
- **Chart Rendering**: Optimized ApexCharts configuration
- **API Efficiency**: Minimal polling frequency for status updates
- **Caching**: Appropriate caching of static assets and API responses

## Environment Configuration
- **`API_BASE`**: Backend API URL for development/production
- **`FOODPRINT_API_KEY`**: Authentication for API access
- **Build Configuration**: Vite settings for optimal production builds
- **Deployment**: Docker configuration for containerized deployment

The frontend provides an intuitive, educational interface that makes recipe CO₂ emissions understandable and actionable for users, while maintaining clean code architecture and excellent user experience principles.
