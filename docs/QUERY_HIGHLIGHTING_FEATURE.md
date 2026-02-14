# ⭐ Query Highlighting Feature

## 🎯 What's New

Now when you search for objects, **only the queried objects are highlighted** while other objects are shown in gray for context!

## ✨ Visual Differences

### Before (All Objects Highlighted)
```
All objects shown with bright colors:
🟢 Person (bright green, thick box)
🔵 Car (bright blue, thick box)
🟠 Backpack (bright orange, thick box)
🔵 Chair (bright cyan, thick box)
```

### After (Only Queried Objects Highlighted)
```
Query: "person with backpack"

Queried objects (HIGHLIGHTED):
🟢 Person (BRIGHT GREEN, THICK box, YELLOW label)
🟠 Backpack (BRIGHT ORANGE, THICK box, YELLOW label)

Other objects (for context):
⚪ Car (gray, thin box, small label)
⚪ Chair (gray, thin box, small label)
```

## 🎨 Visual Indicators

### Queried Objects (What You Searched For)
- ✅ **Thick bounding box** (4px width)
- ✅ **Bright colors** (Green, Blue, Orange, Cyan)
- ✅ **Yellow background label** with black text
- ✅ **>>> UPPERCASE <<< format** (e.g., ">>> PERSON <<<")
- ✅ **Large font** (0.8 scale)
- ✅ **Star badge** (⭐) in results list
- ✅ **Golden border** on badge
- ✅ **Pulse animation** on badge

### Other Objects (For Context)
- ⚪ **Thin bounding box** (1px width)
- ⚪ **Gray color** (128, 128, 128)
- ⚪ **Gray background label** with white text
- ⚪ **lowercase format** (e.g., "car")
- ⚪ **Small font** (0.4 scale)
- ⚪ **No special effects**

## 📊 Example Scenarios

### Scenario 1: Search for "person"

**Query:** `person`

**Image Annotation:**
```
┌─────────────────────────────────────┐
│                                     │
│  ┏━━━━━━━━━━━┓  ┌─────────┐        │
│  ┃           ┃  │         │        │
│  ┃ >>> PERSON <<<│   car   │        │
│  ┃  (BRIGHT) ┃  │ (gray)  │        │
│  ┃           ┃  └─────────┘        │
│  ┗━━━━━━━━━━━┛                     │
│                                     │
└─────────────────────────────────────┘

Legend:
┏━━━┓ = Thick bright box (queried)
┌───┐ = Thin gray box (other)
```

**Badge Display:**
```
🔍 Detected: [person ⭐] [car]
              ↑           ↑
         Highlighted   Normal
         (golden       (regular
          border)       badge)
```

### Scenario 2: Search for "person with backpack"

**Query:** `person with backpack`

**Image Annotation:**
```
┌─────────────────────────────────────┐
│                                     │
│  ┏━━━━━━━━━━━┓                     │
│  ┃>>> PERSON <<<                   │
│  ┃           ┃  ┏━━━━━━━━━━━┓     │
│  ┃  (BRIGHT) ┃  ┃>>> BACKPACK <<<  │
│  ┃           ┃  ┃  (BRIGHT)  ┃     │
│  ┗━━━━━━━━━━━┛  ┗━━━━━━━━━━━┛     │
│                                     │
│  ┌─────────┐  ┌─────────┐         │
│  │  chair  │  │  table  │         │
│  │ (gray)  │  │ (gray)  │         │
│  └─────────┘  └─────────┘         │
└─────────────────────────────────────┘

Both person and backpack highlighted!
Chair and table shown in gray for context.
```

**Badge Display:**
```
🔍 Detected: [person ⭐] [backpack ⭐] [chair] [table]
              ↑            ↑           ↑       ↑
         Highlighted   Highlighted  Normal  Normal
```

### Scenario 3: Search for "car"

**Query:** `car`

**Image Annotation:**
```
┌─────────────────────────────────────┐
│                                     │
│  ┌─────────┐  ┏━━━━━━━━━━━┓        │
│  │ person  │  ┃>>> CAR <<<┃        │
│  │ (gray)  │  ┃  (BRIGHT) ┃        │
│  └─────────┘  ┗━━━━━━━━━━━┛        │
│                                     │
│  ┌─────────┐                        │
│  │  truck  │                        │
│  │ (gray)  │                        │
│  └─────────┘                        │
└─────────────────────────────────────┘

Only car is highlighted!
Person and truck shown in gray.
```

## 🎯 How It Works

### Backend (main.py)

```python
# Parse query to extract object names
query_objects = ["person", "backpack"]  # From "person with backpack"

# For each detected object:
if object matches query:
    # Highlight it
    thickness = 4
    color = bright_color
    label = ">>> OBJECT <<<"
else:
    # Show in gray
    thickness = 1
    color = gray
    label = "object"
```

### Frontend (dashboard.html)

```javascript
// Add query parameter to image URL
const annotatedImageUrl = `/annotated_image/${frameFilename}?query=${searchQuery}`;

// Highlight badges for queried objects
if (queryLower.includes(obj.toLowerCase())) {
    badge += ' ⭐';  // Add star
    badge.style = 'border: 2px solid #ffc107';  // Golden border
}
```

## 🎨 Color Scheme

### Queried Objects (Bright)
- **Person**: Bright Green (0, 255, 0)
- **Car**: Bright Blue (255, 0, 0)
- **Backpack**: Bright Orange (0, 165, 255)
- **Other**: Bright Cyan (255, 255, 0)

### Label Background (Queried)
- **Background**: Yellow (0, 255, 255)
- **Text**: Black (0, 0, 0)
- **Font**: Bold, Large (0.8 scale)

### Other Objects (Gray)
- **Box**: Gray (128, 128, 128)
- **Background**: Gray (128, 128, 128)
- **Text**: White (255, 255, 255)
- **Font**: Small (0.4 scale)

## 💡 Benefits

### 1. Focus on What Matters
- See exactly what you searched for
- Ignore irrelevant objects
- Quick visual identification

### 2. Context Awareness
- Still see other objects
- Understand scene composition
- Verify detection accuracy

### 3. Professional Look
- Clear visual hierarchy
- Easy to understand
- Impressive in demos

### 4. Better Analysis
- Track specific objects
- Compare across frames
- Identify patterns

## 🎯 Use Cases

### Security Monitoring
```
Query: "person with backpack"
Result: Quickly spot people carrying bags
Context: See other people and objects nearby
```

### Parking Management
```
Query: "car"
Result: Highlight all cars
Context: See trucks, motorcycles in gray
```

### Lost Items
```
Query: "backpack"
Result: Highlight all backpacks
Context: See if person is nearby (gray)
```

### Crowd Analysis
```
Query: "person"
Result: Highlight all people
Context: See furniture, vehicles in gray
```

## 🚀 How to Use

### Step 1: Upload Video
```
Upload any video with multiple objects
```

### Step 2: Search
```
Query: "person"
or
Query: "person with backpack"
or
Query: "car"
```

### Step 3: View Results
```
Images show:
- Queried objects: BRIGHT, THICK boxes
- Other objects: Gray, thin boxes
- Badges: Stars on queried objects
```

### Step 4: Analyze
```
- Focus on highlighted objects
- Use gray objects for context
- Click to jump to video
```

## 📊 Comparison

### Old System
```
All objects equally highlighted
Hard to focus on what you searched for
Visual clutter
```

### New System
```
✅ Queried objects stand out
✅ Other objects provide context
✅ Clear visual hierarchy
✅ Easy to analyze
```

## 🎉 Result

Now you can:
- ✅ **Instantly spot** queried objects
- ✅ **See context** with other objects
- ✅ **Focus attention** on what matters
- ✅ **Analyze faster** with clear visuals
- ✅ **Impress viewers** with professional output

**The system now intelligently highlights only what you're looking for!** ⭐🎯

---

**Try it now:**
1. Upload a video
2. Search for "person"
3. See persons highlighted in bright colors
4. See other objects in gray for context
5. Notice the ⭐ stars on queried object badges!
