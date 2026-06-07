# health_data.py

HEALTH_RULES = {
    "good_foods": {
        "keywords": ["good food", "healthy food", "what to eat", "recommendation", "millet"],
        "response": "Incorporate traditional Indian items like Ragi Java (great for calcium and cooling), Pearl Millet (Bajra), Foxtail Millet, leafy greens, and lentils. They are rich in fiber and keep your blood sugar stable."
    },
    "bad_foods": {
        "keywords": ["bad food", "avoid", "unhealthy", "junk"],
        "response": "Try to avoid refined flour (maida), excess white sugar, deep-fried snacks like samosas, and highly processed packed foods. Switch white rice with brown rice or millets where possible."
    },
    "ragi_java": {
        "keywords": ["ragi java", "ragi", "how to make ragi"],
        "response": "Ragi Java is a superfood! Boil 2 tbsp of ragi flour in water, stir continuously to avoid lumps, and add buttermilk with salt, or milk with jaggery. Great for breakfast!"
    },
    "diet_plan": {
        "keywords": ["diet plan", "routine", "meal plan", "what should i eat today"],
        "response": "Here is a healthy Indian Diet Plan:\n- *Breakfast:* Ragi Java or Oats Idli with mint chutney.\n- *Lunch:* Brown rice or Jowar roti with a bowl of dal and mixed vegetable sabzi.\n- *Snack:* A handful of roasted chana or a fruit.\n- *Dinner:* Light Millet khichdi or vegetable soup."
    }
}

DEFAULT_RESPONSE = "I'm a rule-based health assistant. Try asking me about 'good food', 'bad food', 'ragi java', or request a 'diet plan'!"
