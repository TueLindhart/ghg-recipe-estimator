# Learnings

This file collects observations about how the repository is organized, coding preferences, architectural decisions, and accumulated development context that emerge over time.

## Project Architecture & Principles

### Coding Standards
- **Python Formatting**: Code formatted with [Ruff](https://github.com/astral-sh/ruff) and checked with `pyright`
- **Line Length**: 88 characters as configured in `pyproject.toml`
- **Type Hints**: Comprehensive type hinting across all Python functions
- **SOLID Principles**: Clean separation of concerns, single responsibility pattern
- **Readability**: Code prioritizes clarity and maintainability over cleverness

### Asynchronous Design Philosophy
- **Backend Operations**: Many functions, especially in the estimator, are asynchronous
- **Testing**: Uses `pytest` with `pytest-asyncio` for async function testing
- **API Design**: FastAPI with background tasks for long-running operations
- **Frontend Integration**: Non-blocking job management with polling patterns

### Configuration Management
- **Environment Variables**: Configuration such as API keys, cache options and model vendor read from environment
- **Template Configuration**: `template.env` shows all required environment keys
- **Flexible Deployment**: Local development and production deployment configurations
- **Service Dependencies**: Graceful degradation when optional services unavailable

### Caching Strategy
- **Multi-layer Caching**: Results cached in Google Cloud Storage for persistence
- **Redis Integration**: Job status, rate limiting, and temporary data storage
- **Cache Control**: `USE_CACHE` and `STORE_IN_CACHE` flags for development flexibility
- **Performance**: Reduces API calls and improves response times significantly

## Data Architecture & Sources

### Emission Spreadsheet Structure
The `data/DBv2.xlsx` file contains CO₂ emission information with:
- **Sheet Organization**: `DK` sheet for Danish data, `GB` for English
- **Primary Source**: DK sheet used for emission enrichment
- **Column Headers**: `ID_Ra`, `Navn`, `DSK Kategori`, `Produkt`, `Kategori`, `Total kg CO2e/kg`
- **Emission Breakdown**: `Landbrug`, `ILUC`, `Forarbejdning`, `Emballage`, `Transport`, `Detail`
- **Nutritional Data**: `Energi (KJ/100 g)`, `Fedt (g/100 g)`, `Kulhydrat (g/100 g)`, `Protein (g/100 g)`
- **Database Keys**: `ID_food`, `ID_pack`, `ID_retail` for cross-referencing

### API Response Architecture
- **Separation of Concerns**: Comparison endpoint separated from recipe results
- **Climate Budgets**: Constants for budgets and average emissions exposed via dedicated endpoint
- **Data Normalization**: Emission factors standardized for consistent frontend consumption
- **Nutritional Integration**: Complete nutritional data included in all recipe responses

## Frontend Design Philosophy & User Preferences

### Component Architecture Pattern
- **Info Icon Consistency**: Card with `relative` positioning, info button at `absolute top-2 right-2`
- **Prop Flexibility**: `cardClass` pattern allows layout control while preserving core styling
- **Text Hierarchy**: `text-2xl font-bold` for primary numbers, `text-sm mt-1` for labels
- **Height Management**: Components use `min-h-80` with `py-12` padding for visual consistency

### Layout Requirements (User Validated)
- **Vertical Organization**: Tabs positioned above content using `flex flex-col`, not beside
- **Desktop Sizing**: Cards should be compact (1/3 to 1/2 screen width), not full-width stretching
- **Responsive Design**: Mobile-first approach with desktop enhancements
- **Overview Prominence**: `co2_per_person_kg` displayed prominently with larger font sizes

### Visual Hierarchy Principles
- **Primary Numbers**: Must be visually dominant (`text-3xl font-bold` or larger) and centered
- **Supporting Text**: Clearly secondary but readable (`text-sm`)
- **Proportional Sizing**: Significant size difference between primary and secondary elements
- **Spacing Standards**: Subtle spacing adjustments, consistent gap patterns

### User Experience Insights
- **Iterative Design Process**: User prefers incremental changes with visual confirmation
- **Visual Feedback**: Screenshots and live previews essential for design decisions
- **Quick Adjustments**: Frequent small styling changes (fonts, spacing, alignment)
- **Educational Focus**: Information should be accessible but not overwhelming

## Technology Integration Learnings

### Flowbite Svelte Component Library
- **Tabs Component**: `tabStyle="underline"` provides clean professional appearance
- **Chart Integration**: ApexCharts wrapper works well for data visualization
- **Card Flexibility**: Excellent base component with comprehensive customization options
- **Modal Patterns**: Consistent structure for additional information display

### Backend-Frontend Integration
- **Job Management**: UUID-based job tracking with Redis persistence works reliably
- **Status Polling**: Granular status updates (EXTRACTING_TEXT, ESTIMATING_WEIGHTS, etc.)
- **Error Handling**: Comprehensive error states with user-friendly messages
- **Rate Limiting**: Redis-based rate limiting protects against abuse

### Performance Optimization
- **Component Loading**: Efficient Svelte component imports and rendering
- **Chart Performance**: Optimized ApexCharts configuration for responsive updates
- **API Efficiency**: Minimal polling frequency while maintaining real-time feel
- **Caching Strategy**: Multiple layers reduce load times and improve user experience

## Development Process Insights

### Design Iteration Pattern
- **User-Centered**: Regular feedback cycles with visual confirmation of changes
- **Component-First**: Build individual components, then compose into layouts
- **Responsive Testing**: Test across device sizes during development
- **Pattern Establishment**: Document successful patterns for reuse

### Code Organization Success Factors
- **Clear Separation**: Frontend, backend, and estimation logic cleanly separated
- **Type Safety**: TypeScript interfaces ensure data consistency
- **Error Boundaries**: Graceful error handling at all system levels
- **Documentation**: Comprehensive documentation enables team collaboration

### Deployment & Operations
- **Container Strategy**: Docker with multi-stage builds for optimal size
- **Environment Management**: Clear separation of development and production configs
- **Monitoring**: Structured logging for debugging and production monitoring
- **Health Checks**: Basic health endpoints for deployment verification

Further insights should be appended here as the code evolves.
