# Foodprint Styling Guide

## Technology Stack
- Tailwind CSS for utility-based styling
- Flowbite Svelte for pre-built components
- Flowbite Svelte Icons for iconography

## Color System
### Text Colors
- Primary text: `text-[#404040]`
- Secondary/muted text: `text-gray-500`
- Interactive hover: `hover:text-gray-700`
- Font weights: `font-semibold` for headers, normal for body text
- Sizes: `text-sm` for body, `text-md` for subheadings, `text-2xl` for main headers, `text-3xl` for large numbers

## Component Patterns

### Card Components
```svelte
<Card class="p-6 relative min-h-80">
  <!-- Content -->
</Card>
```
- Use Flowbite's Card component as base
- Standard padding: `p-6` for main content cards
- Use `relative` positioning for parent containers with info icons
- Tab components: `min-h-80` with `py-12` for adequate content space
- **Critical**: Pass styling through `cardClass` prop, never hardcode in components

### Layout Spacing
- Vertical rhythm:
  - `mb-4` for standard block spacing
  - `mb-8` for major section breaks
  - `mt-8` for major section starts
  - `gap-4` for flex container item spacing
  - `gap-6` for larger flex container spacing

### Interactive Elements
- Buttons: Use `BaseButton` component or Flowbite's `Button`
- Focus states: `focus:outline-none`
- Hover states: `hover:text-gray-700`
- Include `aria-label` for accessibility

### Containers & Grid
- Page container: `container mx-auto px-4`
- Flex layouts:
  - `flex flex-col lg:flex-row` for responsive column-to-row layouts
  - `flex flex-wrap` for wrapping content
  - `items-center` for vertical alignment
  - `justify-between` for space distribution

### Responsive Design
- Mobile-first approach with breakpoint modifiers:
  - `lg:flex-row` for desktop layouts
  - `sm:basis-auto` for fluid sizing
  - `md:max-h-[400px]` for controlled heights
- Use relative units when possible

### Tabs
- Use Flowbite's `Tabs` with `tabStyle="pill"`
- Consistent container spacing:
```svelte
<Tabs class="mt-8" tabStyle="pill">
  <TabItem title="Title" open>
    <!-- Content -->
  </TabItem>
</Tabs>
```

### Scrollable Content
```svelte
<div class="min-h-[300px] max-h-[400px] md:max-h-[400px] overflow-y-auto">
  <!-- Scrollable content -->
</div>
```

## Best Practices
1. Always use Flowbite components when available
2. Maintain consistent spacing using Tailwind's scale
3. Use semantic HTML elements with appropriate ARIA attributes
4. Follow mobile-first responsive design patterns
5. Keep text styles consistent using the defined size and weight system
6. **Pass styling through component props** - use `cardClass` for height/padding customization
7. **Never hardcode styling** in components - maintain flexibility through props
8. **Follow documentation patterns** - consistency is critical for maintainability
