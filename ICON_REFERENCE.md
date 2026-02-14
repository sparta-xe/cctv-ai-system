# 🎨 ICON REFERENCE GUIDE

## 📋 Complete Icon List

### Header Section
```html
<i data-lucide="video" class="icon-lg"></i>
```
**Purpose:** Main logo/brand icon

---

### Stats Cards (with pulse)
```html
<!-- Total Frames -->
<i data-lucide="layers" class="icon icon-pulse"></i>

<!-- Detections -->
<i data-lucide="scan" class="icon icon-pulse"></i>

<!-- Alerts -->
<i data-lucide="alert-triangle" class="icon icon-pulse"></i>

<!-- Accuracy -->
<i data-lucide="target" class="icon icon-pulse"></i>
```
**Purpose:** Animated stat indicators

---

### Upload Section
```html
<!-- Section title -->
<i data-lucide="upload-cloud" class="icon-lg"></i>

<!-- File upload area -->
<i data-lucide="file-video" class="icon-lg mx-auto mb-3 w-12 h-12"></i>

<!-- Process button -->
<i data-lucide="cpu" class="icon"></i>
```
**Purpose:** Upload workflow icons

---

### Search Section
```html
<!-- Section title -->
<i data-lucide="search" class="icon-lg"></i>

<!-- Input field left -->
<i data-lucide="sparkles" class="icon absolute left-4 top-3.5"></i>

<!-- Input field right -->
<i data-lucide="zap" class="icon absolute right-4 top-3.5"></i>

<!-- Search button -->
<i data-lucide="brain" class="icon"></i>
```
**Purpose:** AI search interface

---

### Results Section
```html
<!-- Section title -->
<i data-lucide="list-checks" class="icon-lg"></i>
```
**Purpose:** Results display

---

### Video Player
```html
<!-- Section title -->
<i data-lucide="play-circle" class="icon-lg"></i>
```
**Purpose:** Video playback

---

### Alerts Panel
```html
<!-- Section title -->
<i data-lucide="shield-alert" class="icon-lg"></i>

<!-- No alerts state -->
<i data-lucide="check-circle" class="icon"></i>

<!-- Alert items (dynamic) -->
<i data-lucide="alert-circle" class="icon"></i>
```
**Purpose:** Alert notifications

---

### System Status
```html
<!-- Section title -->
<i data-lucide="activity" class="icon-lg"></i>

<!-- CLIP Engine -->
<i data-lucide="eye" class="icon"></i>

<!-- Hybrid Search -->
<i data-lucide="zap" class="icon"></i>

<!-- Device -->
<i data-lucide="cpu" class="icon"></i>

<!-- Model -->
<i data-lucide="brain" class="icon"></i>
```
**Purpose:** System information

---

## 🎯 Icon Classes

### Standard Icon
```html
<i data-lucide="icon-name" class="icon"></i>
```
- Size: 20x20px
- Color: Cyan (#38bdf8)
- Hover: Blue glow

### Large Icon
```html
<i data-lucide="icon-name" class="icon-lg"></i>
```
- Size: 24x24px
- Color: Cyan (#38bdf8)
- Hover: Blue glow

### Pulsing Icon
```html
<i data-lucide="icon-name" class="icon icon-pulse"></i>
```
- Animated glow pulse
- 2s cycle
- Draws attention

---

## 🌟 Popular Lucide Icons

### Navigation
- `home` - Home
- `layout-dashboard` - Dashboard
- `search` - Search
- `settings` - Settings
- `menu` - Menu

### Actions
- `upload` - Upload
- `download` - Download
- `play` - Play
- `pause` - Pause
- `refresh-cw` - Refresh

### Status
- `check-circle` - Success
- `alert-circle` - Warning
- `x-circle` - Error
- `info` - Information
- `help-circle` - Help

### Media
- `video` - Video
- `camera` - Camera
- `image` - Image
- `film` - Film
- `play-circle` - Play

### Tech
- `cpu` - Processor
- `brain` - AI/ML
- `zap` - Lightning/Fast
- `activity` - Activity
- `eye` - Vision

### Security
- `shield` - Shield
- `shield-alert` - Alert
- `lock` - Lock
- `unlock` - Unlock
- `key` - Key

### Data
- `database` - Database
- `server` - Server
- `hard-drive` - Storage
- `layers` - Layers
- `scan` - Scan

---

## 🎨 Customization

### Change Color
```css
.icon {
    stroke: #ff0000; /* Red */
}
```

### Change Size
```css
.icon {
    width: 32px;
    height: 32px;
}
```

### Add Glow
```css
.icon {
    filter: drop-shadow(0 0 10px #38bdf8);
}
```

### Rotate
```css
.icon {
    transform: rotate(45deg);
}
```

---

## 🔧 Dynamic Icons

### Add Icon to Dynamic Content
```javascript
// After adding HTML with icons
lucide.createIcons();
```

### Example
```javascript
alertsList.innerHTML = `
    <div class="alert">
        <i data-lucide="alert-circle" class="icon"></i>
        Alert message
    </div>
`;

// Re-initialize icons
lucide.createIcons();
```

---

## 📚 Full Icon Library

Browse all icons: https://lucide.dev/icons/

### Categories
- **Arrows**: arrow-right, arrow-left, chevron-down
- **Communication**: mail, message-circle, phone
- **Files**: file, folder, file-text
- **Media**: video, camera, image
- **Navigation**: home, menu, search
- **Status**: check, x, alert-triangle
- **Tech**: cpu, wifi, bluetooth
- **UI**: plus, minus, edit

---

## ✅ Best Practices

1. **Consistency**: Use same icon for same action
2. **Size**: Use icon-lg for titles, icon for inline
3. **Color**: Stick to cyan/blue theme
4. **Animation**: Use pulse sparingly (important items only)
5. **Accessibility**: Add aria-label for screen readers

### Example with Accessibility
```html
<i data-lucide="search" class="icon" aria-label="Search"></i>
```

---

## 🚀 Quick Reference

### Most Used Icons
```
video          - Video/Camera
search         - Search
upload-cloud   - Upload
brain          - AI
cpu            - Processing
alert-triangle - Warning
check-circle   - Success
zap            - Fast/Power
eye            - Vision
shield-alert   - Security
```

### Icon Sizes
```
icon      - 20x20px (standard)
icon-lg   - 24x24px (titles)
w-12 h-12 - 48x48px (large displays)
```

### Animations
```
icon-pulse     - Pulsing glow
hover:scale-110 - Scale on hover
animate-spin   - Rotating
```

---

## 🎯 Pro Tips

1. **Loading States**: Use `loader` icon with `animate-spin`
2. **Success**: Use `check-circle` with green color
3. **Error**: Use `x-circle` with red color
4. **Info**: Use `info` with blue color
5. **Warning**: Use `alert-triangle` with yellow color

### Example Loading Button
```html
<button class="btn-glow">
    <i data-lucide="loader" class="icon animate-spin"></i>
    Processing...
</button>
```

---

## 🏆 Result

With Lucide icons, your dashboard has:
- ✅ Modern, clean aesthetic
- ✅ Consistent design language
- ✅ Professional polish
- ✅ Lightweight (no heavy icon fonts)
- ✅ Easy to customize

**Perfect match for the cyber theme!** 🌌✨
