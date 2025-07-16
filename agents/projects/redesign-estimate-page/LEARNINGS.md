# Learnings About the User's Preferences and Feedback

## General UI Preferences (User)
- The user prefers clear, readable layouts with good hierarchy and spacing.
- The user wants the most important numbers (CO2 per person) to be visually dominant and centered.
- Supporting text (units, summary) should be visually secondary, but still readable and well-aligned according to the user.
- The user values proportional sizing: big numbers should be much bigger than supporting text, but not excessively so.
- The user wants the card to avoid excessive width on large screens, preferring a more compact look.

## Specific Component Feedback (OverviewCard)
- The user wants the big CO2 number to be very large (now 1.5x bigger than before), centered vertically and horizontally.
- The unit label ("kg CO2e pr. person") should be directly below the number, same size as before, and not too small or too large, per the user's preference.
- The summary text ("x kg co2e for x personer") should be readable, about 1.25x bigger than default, and aligned at the bottom of the card, as the user prefers.
- The user does not want the summary text to be bold.
- The user wants the card width to be about half or a third of the screen on laptops, not stretching too wide.
- The user prefers subtle spacing adjustments (not too much, not too little) between number and unit.
- The user iterates quickly and values seeing visual changes before deciding on final details.

## Design Process (User)
- The user often changes their mind after seeing the result, and prefers to experiment with size, spacing, and alignment until it feels right.
- The user provides feedback based on screenshots and live previews, not just code.
- The user wants changes to be made incrementally and responsively to their feedback.

---

## Learnings About Flowbite Svelte Tabs Component

### Basic Usage
- Import with:  
  `import { Tabs, TabItem } from "flowbite-svelte";`
- Wrap tab content in `<Tabs>`, each tab in `<TabItem>`.
- Use `title="..."` for simple tab labels, or use the `titleSlot` for custom tab headers (e.g. icons, custom markup).
- Example:
  ```svelte
  <Tabs>
    <TabItem open title="Profile">
      <p>Profile content here</p>
    </TabItem>
    <TabItem title="Settings">
      <p>Settings content here</p>
    </TabItem>
  </Tabs>
  ```

### Styling Tabs
- Use `tabStyle` prop on `<Tabs>` for built-in styles:
  - `"underline"`: Underline active tab.
  - `"pill"`: Pill-shaped tabs.
  - `"full"`: Tabs stretch to full width of parent.
- You can further customize tab appearance with `activeClass` and `inactiveClass` props on `<TabItem>`.
- Example:
  ```svelte
  <Tabs tabStyle="underline">
    <TabItem title="Profile">...</TabItem>
  </Tabs>
  ```

### Styling Tab Content
- Style tab content using Tailwind CSS classes directly inside each `<TabItem>`.
- Example:
  ```svelte
  <TabItem title="Profile">
    <div class="text-3xl font-bold text-center my-4">Big Number</div>
    <div class="text-base text-gray-500 mt-2">Supporting text</div>
  </TabItem>
  ```
- You can add any Svelte component or markup inside `<TabItem>`.

### Advanced Features
- Tabs can be disabled with the `disabled` prop.
- Use icons in tab headers via the `titleSlot`.
- You can add other Flowbite components (e.g. Timeline, Button) inside tab content.

### Props Reference
- `<Tabs>` props: `tabStyle`, `ulClass`, `contentClass`, `divider`.
- `<TabItem>` props: `title`, `open`, `activeClass`, `inactiveClass`, `class`, `disabled`.

###
