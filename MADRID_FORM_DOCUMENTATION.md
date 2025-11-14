# Madrid Marble Contact Form - Complete Documentation

## Overview
This document provides a comprehensive overview of the Madrid Marble contact form setup, including typography, color scheme, styling, and all form content configurations.

---

## Typography & Fonts

### Primary Font Family
- **Font Stack**: `font-sans` (Tailwind CSS default)
  - Uses system fonts: `ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif`
- **Base Font Size**: `text-lg` (18px / 1.125rem)
- **Font Weight**: Regular (400) for body text, `font-semibold` (600) for labels and headings
- **Text Rendering**: `antialiased` for smooth font rendering

### Icon Font
- **Font Awesome**: Version 6.5.0
- **CDN**: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css`
- Used for contact information icons and form elements

### Typography Scale
- **Form Labels**: `text-base` (16px) with `font-semibold`
- **Form Inputs**: `text-gray-900` (inherits base size)
- **Form Button**: `text-lg` (18px) with `font-semibold`
- **Disclaimer Text**: `text-base` (16px)
- **Section Heading**: `text-4xl` (36px) on mobile, `text-5xl` (48px) on medium+ screens

---

## Color Palette

### Form Container
- **Background**: `bg-white` (#FFFFFF)
- **Border Radius**: `rounded-3xl` (24px)
- **Padding**: 
  - Mobile: `p-8` (32px)
  - Desktop: `md:p-10` (40px)
- **Shadow**: `shadow-2xl` (large shadow for depth)

### Form Section Background
- **Section Background**: `bg-gray-950` (#030712)
- **Overlay**: `bg-gray-950/90` (90% opacity dark overlay)
- **Text Color**: `text-gray-100` (#F3F4F6) for main text
- **Secondary Text**: `text-gray-200` (#E5E7EB) for descriptions
- **Tertiary Text**: `text-gray-300` (#D1D5DB) for contact info

### Form Fields

#### Labels
- **Color**: `text-gray-700` (#374151)
- **Font Weight**: `font-semibold` (600)
- **Font Size**: `text-base` (16px)

#### Input Fields & Textarea
- **Text Color**: `text-gray-900` (#111827)
- **Border Color (Default)**: `border-gray-200` (#E5E7EB)
- **Border Color (Focus)**: `border-gray-900` (#111827)
- **Background**: White (inherited from container)
- **Padding**: `px-5 py-3.5` (20px horizontal, 14px vertical)
- **Border Radius**: `rounded-xl` (12px)
- **Focus Ring**: `focus:ring-2 focus:ring-gray-900/20` (2px ring with 20% opacity)

#### Submit Button
- **Background**: `bg-gray-900` (#111827)
- **Hover Background**: `hover:bg-black` (#000000)
- **Text Color**: `text-white` (#FFFFFF)
- **Font Weight**: `font-semibold` (600)
- **Font Size**: `text-lg` (18px)
- **Padding**: `px-7 py-3.5` (28px horizontal, 14px vertical)
- **Border Radius**: `rounded-xl` (12px)
- **Transition**: Smooth color transition on hover

#### Disclaimer Text
- **Color**: `text-gray-500` (#6B7280)
- **Font Size**: `text-base` (16px)

### Contact Information Icons
- **Icon Color**: `text-gray-400` (#9CA3AF)
- **Icon Size**: `text-lg` (18px)
- **Link Hover**: `hover:text-white` (#FFFFFF)

### Social Media Icons
- **Border Color**: `border-gray-800` (#1F2937)
- **Text Color**: `text-gray-400` (#9CA3AF)
- **Hover Border**: `hover:border-white` (#FFFFFF)
- **Hover Text**: `hover:text-white` (#FFFFFF)
- **Size**: `h-12 w-12` (48px × 48px)
- **Border Radius**: `rounded-full` (fully rounded)

---

## Form Structure & Layout

### Grid System
- **Container**: `max-w-6xl` (1152px max width)
- **Grid Layout**: 
  - Mobile: Single column
  - Desktop (`lg:`): Two columns `lg:grid-cols-[1.1fr_1.2fr]`
  - Gap: `lg:gap-16` (64px between columns)

### Form Fields Grid
- **Grid**: `md:grid-cols-2` (2 columns on medium+ screens)
- **Gap**: `gap-7` (28px between fields)
- **Field Spacing**: `space-y-7` (28px vertical spacing)

---

## Form Fields Configuration

### Field 1: Name
```json
{
  "name": "name",
  "label": "Name",
  "type": "text",
  "placeholder": "Your full name",
  "span": 1
}
```
- **Grid Span**: 1 column (half width on desktop)
- **Input Type**: Text
- **Placeholder**: "Your full name"

### Field 2: Email
```json
{
  "name": "email",
  "label": "Email",
  "type": "email",
  "placeholder": "name@company.com",
  "span": 1
}
```
- **Grid Span**: 1 column (half width on desktop)
- **Input Type**: Email (with browser validation)
- **Placeholder**: "name@company.com"

### Field 3: Phone
```json
{
  "name": "phone",
  "label": "Phone",
  "type": "tel",
  "placeholder": "+971 50 000 0000",
  "span": 2
}
```
- **Grid Span**: 2 columns (full width on desktop)
- **Input Type**: Tel (telephone)
- **Placeholder**: "+971 50 000 0000" (UAE format)

### Field 4: Message
```json
{
  "name": "message",
  "label": "Message",
  "type": "textarea",
  "placeholder": "Share your project scope, timelines, and preferred marble finishes.",
  "rows": 5,
  "span": 2
}
```
- **Grid Span**: 2 columns (full width on desktop)
- **Input Type**: Textarea
- **Rows**: 5
- **Placeholder**: "Share your project scope, timelines, and preferred marble finishes."

### Submit Button
```json
{
  "label": "Submit inquiry"
}
```
- **Width**: Full width (`w-full`)
- **Text**: "Submit inquiry"

### Disclaimer
```json
{
  "disclaimer": "By submitting this form you agree to be contacted regarding Madrid Marble services."
}
```
- **Text**: "By submitting this form you agree to be contacted regarding Madrid Marble services."

---

## Contact Information Section

### Location
- **Icon**: `fa-solid fa-location-dot`
- **Text**: "Warehouse 4, Dubai Investment Park 2, UAE"
- **Type**: Static text (no link)

### Email
- **Icon**: `fa-solid fa-envelope`
- **Text**: "hello@madridmarble.ae"
- **Link**: `mailto:hello@madridmarble.ae`
- **Hover Effect**: Text color changes to white

### Phone
- **Icon**: `fa-solid fa-phone`
- **Text**: "+971 4 422 3355"
- **Link**: `tel:+97144223355`
- **Hover Effect**: Text color changes to white

### Social Media Links
1. **Instagram**: `fa-brands fa-instagram` (placeholder link: `#`)
2. **TikTok**: `fa-brands fa-tiktok` (placeholder link: `#`)
3. **LinkedIn**: `fa-brands fa-linkedin-in` (placeholder link: `#`)

---

## Section Styling Details

### Section Container
- **ID**: `#contact`
- **Position**: `relative` with `overflow-hidden`
- **Background**: `bg-gray-950` with optional background image
- **Padding**: `py-24` (96px vertical padding)
- **Text Color**: `text-gray-100`

### Background Image
- **Source**: `https://images.unsplash.com/photo-1560769629-975ec94e6a86?auto=format&fit=crop&w=1400&q=70`
- **Style**: Cover, centered
- **Overlay**: Dark overlay at 90% opacity for text readability

### Section Heading
- **Text**: "Get in touch"
- **Size**: `text-4xl` (36px) on mobile, `text-5xl` (48px) on desktop
- **Weight**: `font-semibold` (600)
- **Color**: Inherits section text color (`text-gray-100`)

### Section Description
- **Text**: "For inquiries or showroom appointments, contact our team. We respond within 24 hours with tailored recommendations and availability."
- **Size**: `text-lg` (18px)
- **Color**: `text-gray-200`

---

## Responsive Design

### Breakpoints
- **Mobile**: Default (base styles)
- **Medium (`md:`)**: 768px and above
  - Form grid switches to 2 columns
  - Padding increases on form container
- **Large (`lg:`)**: 1024px and above
  - Section switches to 2-column layout
  - Contact info on left, form on right

### Mobile Optimizations
- Single column layout for form fields
- Reduced padding on form container (`p-8` vs `md:p-10`)
- Full-width submit button
- Stacked contact information

---

## Form HTML Structure

```html
<form class="space-y-7">
  <div class="grid gap-7 md:grid-cols-2">
    <!-- Name Field -->
    <div class="space-y-2">
      <label for="name" class="text-base font-semibold text-gray-700">Name</label>
      <input id="name" name="name" type="text" placeholder="Your full name" 
             class="w-full rounded-xl border border-gray-200 px-5 py-3.5 text-gray-900 
                    focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900/20">
    </div>
    
    <!-- Email Field -->
    <div class="space-y-2">
      <label for="email" class="text-base font-semibold text-gray-700">Email</label>
      <input id="email" name="email" type="email" placeholder="name@company.com" 
             class="w-full rounded-xl border border-gray-200 px-5 py-3.5 text-gray-900 
                    focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900/20">
    </div>
    
    <!-- Phone Field (Full Width) -->
    <div class="space-y-2 md:col-span-2">
      <label for="phone" class="text-base font-semibold text-gray-700">Phone</label>
      <input id="phone" name="phone" type="tel" placeholder="+971 50 000 0000" 
             class="w-full rounded-xl border border-gray-200 px-5 py-3.5 text-gray-900 
                    focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900/20">
    </div>
    
    <!-- Message Field (Full Width) -->
    <div class="space-y-2 md:col-span-2">
      <label for="message" class="text-base font-semibold text-gray-700">Message</label>
      <textarea id="message" name="message" placeholder="Share your project scope, timelines, and preferred marble finishes." 
                rows="5" 
                class="w-full rounded-xl border border-gray-200 px-5 py-3.5 text-gray-900 
                       focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900/20"></textarea>
    </div>
  </div>
  
  <!-- Submit Button -->
  <button type="submit" 
          class="w-full rounded-xl bg-gray-900 px-7 py-3.5 text-lg font-semibold text-white 
                 transition hover:bg-black">
    Submit inquiry
  </button>
  
  <!-- Disclaimer -->
  <p class="text-base text-gray-500">
    By submitting this form you agree to be contacted regarding Madrid Marble services.
  </p>
</form>
```

---

## CSS Framework & Dependencies

### Tailwind CSS
- **Version**: Latest (via CDN)
- **CDN**: `https://cdn.tailwindcss.com`
- **Configuration**: Default configuration (no custom config file)

### Font Awesome
- **Version**: 6.5.0
- **CDN**: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css`
- **Usage**: Icons for contact information and social media

---

## Accessibility Features

### Form Labels
- All form fields have associated `<label>` elements
- Labels use `for` attribute matching input `id`
- Labels are visually distinct with `font-semibold` and `text-gray-700`

### Focus States
- All inputs have visible focus indicators
- Focus ring: 2px ring with gray-900 at 20% opacity
- Border color changes to `gray-900` on focus
- Outline removed in favor of custom ring

### Input Types
- Semantic HTML input types (`email`, `tel`, `text`, `textarea`)
- Browser-native validation for email fields
- Mobile keyboards adapt to input type (e.g., numeric keypad for phone)

---

## Form Data Structure

The form collects the following data:
1. **name** (string): User's full name
2. **email** (string): User's email address
3. **phone** (string): User's phone number
4. **message** (string): Project details and requirements

---

## File Locations

### Template File
- **Path**: `myProject/myApp/templates/partials/contact.html`
- **Included in**: `myProject/myApp/templates/home.html`

### Content Configuration
- **Path**: `myProject/myApp/content/homepage.json`
- **Section**: `"contact"` (lines 272-342)

### Content Loader
- **Path**: `myProject/myApp/content/homepage.py`
- **Function**: `get_homepage_content()`

### View Handler
- **Path**: `myProject/myApp/views.py`
- **Function**: `home(request)`

---

## Customization Notes

### To Change Colors
1. Update Tailwind classes in `contact.html`
2. Color values follow Tailwind's gray scale (50-950)
3. Primary brand color appears to be `gray-900` (dark)

### To Add/Remove Fields
1. Edit `homepage.json` → `contact.form.fields` array
2. Add/remove field objects with structure:
   ```json
   {
     "name": "field_name",
     "label": "Field Label",
     "type": "text|email|tel|textarea",
     "placeholder": "Placeholder text",
     "span": 1|2,
     "rows": 5  // for textarea only
   }
   ```

### To Modify Styling
- All styles use Tailwind utility classes
- No separate CSS file required
- Custom styles can be added in `<style>` tag in `home.html`

---

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Tailwind CSS CDN provides automatic vendor prefixes
- Font Awesome icons work across all modern browsers
- Responsive design tested on mobile, tablet, and desktop viewports

---

## Summary

The Madrid Marble contact form features:
- **Clean, modern design** with white form container on dark background
- **Professional typography** using system fonts with Font Awesome icons
- **Comprehensive color scheme** using Tailwind's gray palette
- **Responsive layout** adapting from mobile to desktop
- **Four form fields**: Name, Email, Phone, and Message
- **Accessible design** with proper labels and focus states
- **Contact information** displayed alongside the form
- **Social media links** integrated into the contact section

---

*Document generated from codebase analysis*
*Last updated: Based on current codebase state*

