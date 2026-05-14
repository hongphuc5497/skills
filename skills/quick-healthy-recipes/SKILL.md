---
name: quick-healthy-recipes
description: "Generate exactly 3 simple, fast, healthy recipes from food photos, ingredient lists, or cravings. Use for what-to-cook-tonight requests. Don't use for restaurants, meal plans, baking, or medical diets."
license: MIT
effort: medium
metadata:
  version: 1.0.0
  author: "Luong NGUYEN <luongnv89@gmail.com>"
---

# Quick Healthy Recipes

Turn food photos, ingredient lists, or a short cooking desire into **exactly 3** practical recipes that are simple, fast, and healthy enough for a normal weeknight.

## When to use

Use this skill when the user asks things like:

- "what can I cook with this?" plus an image
- "find the best recipe for these ingredients"
- "I have eggs, rice, and spinach — dinner ideas?"
- "I want something healthy and quick tonight"

Do not use it for restaurant recommendations, long meal plans, baking projects, special-diet medical advice, or gourmet cooking that requires advanced technique.

## Core principles

Optimize every answer for:

1. **Simple** — few extra ingredients; favor common pantry items.
2. **Fast** — target 15–30 minutes, max 40 minutes unless the user explicitly wants slow cooking.
3. **Healthy** — include vegetables/fiber, useful protein, and reasonable carbs or fats when possible.
4. **Practical tonight** — no special equipment, rare ingredients, or chef techniques.
5. **Low-friction** — if an ingredient is uncertain, give a safe assumption and an easy substitute.

Common pantry items are acceptable: salt, pepper, oil, butter, garlic, onion, vinegar, lemon, soy sauce, eggs, rice, pasta, bread, beans, yogurt, cheese, herbs, and basic spices.

## Workflow

### 1. Understand the input

If images are provided, inspect them before suggesting recipes. Identify:

- Main ingredient(s)
- Freshness or cleaning concerns
- Parts that cook differently, such as stems vs leaves
- Any visible uncertainty

If text is provided, extract:

- Ingredients available
- Desired dish, cuisine, or constraint
- Timing clues like "tonight", "quick", or "lunch"

Ask a question only when a safety-critical detail is missing. Otherwise, make a reasonable assumption and state it briefly.

### 2. Safety filter

Do not confidently identify or recommend eating high-risk unknown items such as wild mushrooms, unknown berries, spoiled food, raw seafood, or foraged plants. If the food might be unsafe, say so and suggest using only verified ingredients.

Do not give medical nutrition advice. For allergies, pregnancy, diabetes, kidney disease, or other medical constraints, keep guidance general and tell the user to follow their clinician's advice.

### 3. Build 3 recipe options

Create exactly 3 distinct options. Each option should vary by cooking style or meal format, for example:

- Stir-fry / sauté
- Soup / stew
- Bowl / salad / pasta
- Omelet / egg dish
- Sheet-pan / pan-roast

For each recipe, keep ingredient additions short. Prefer one protein booster and one carb/fiber base when the raw ingredients alone are not balanced.

### 4. Rank for tonight

Put the best fit first. The first recipe should usually be the fastest and most realistic with the least extra shopping.

## Output format

Use this exact structure. Keep it concise.

```markdown
Looks like: [ingredient identification or parsed request]
Assumption: [one short assumption, or "none"]

1. [Recipe name] — [time]
Best if: [why this is the top fit]
Extra ingredients: [0–5 common items]
Steps:
- [short step]
- [short step]
- [short step]
Healthy balance: [protein + veg/fiber + carb/fat note]

2. [Recipe name] — [time]
Best if: [why choose it]
Extra ingredients: [0–5 common items]
Steps:
- [short step]
- [short step]
- [short step]
Healthy balance: [protein + veg/fiber + carb/fat note]

3. [Recipe name] — [time]
Best if: [why choose it]
Extra ingredients: [0–5 common items]
Steps:
- [short step]
- [short step]
- [short step]
Healthy balance: [protein + veg/fiber + carb/fat note]

Pick tonight: [one sentence recommendation]
```

## Quality checklist

Before finalizing, check:

- Exactly 3 recipes are present
- Each recipe can be cooked without special equipment
- Extra ingredients are common and limited
- The first recipe is the best fit for tonight
- At least two recipes include a realistic protein path
- Any uncertainty from images is stated rather than hidden

If a recipe fails the checklist, replace it before answering.
