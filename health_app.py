import streamlit as st
import re

# =========================================================================
# 1. BACKEND DATABASE STRUCTURES (Assessment Form Engine)
# =========================================================================
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

HEALTH_MATRIX = {
    "Child (1-12)": {
        "sleep_ideal": "9 to 11 hours",
        "exercise": "60 minutes of active play daily (running, cycling, outdoor games).",
        "avoid": "Packed artificially flavored juices, highly processed maida biscuits, and spicy roadside mixtures.",
        "days": {
            "Monday": {"Breakfast": "Ragi malt with milk & soft idli.", "Lunch": "Soft dal khichdi with ghee.", "Snack": "Banana or apple slices.", "Dinner": "Wheat upma with grated carrots."},
            "Tuesday": {"Breakfast": "Millet porridge with a bit of jaggery.", "Lunch": "Curd rice with mashed carrots.", "Snack": "Homemade ragi biscuits.", "Dinner": "Soft paneer bhurji with a mini chapati."},
            "Wednesday": {"Breakfast": "Boiled eggs or milk with fruit.", "Lunch": "Soft-cooked rice, tomato rasam, and soft potato cubes.", "Snack": "Stewed apple.", "Dinner": "Moong dal soup with broken wheat khichdi."},
            "Thursday": {"Breakfast": "Ragi Java with a little milk.", "Lunch": "Vegetable khichdi with curd.", "Snack": "Roasted makhana (fox nuts).", "Dinner": "Soft vermicelli upma with peas."},
            "Friday": {"Breakfast": "Oats porridge with mashed banana.", "Lunch": "Mashed rice, leafy green dal, and ghee.", "Snack": "Fresh curd with honey.", "Dinner": "Paneer cubes with soft wheat dahlia upma."},
            "Saturday": {"Breakfast": "Wheat pancake (Dosa style) with milk.", "Lunch": "Sambar rice with soft-cooked pumpkin.", "Snack": "A handful of boiled sweet corn.", "Dinner": "Light vegetable clear soup and idli."},
            "Sunday": {"Breakfast": "Ragi vermicelli sweet semiya.", "Lunch": "Soft rice, chicken clear soup (non-veg) OR thick paneer dal.", "Snack": "Fruit smoothie.", "Dinner": "Soft-cooked broken rice khichdi."}
        }
    },
    "Teenager (13-19)": {
        "sleep_ideal": "8 to 10 hours",
        "exercise": "60 minutes of physical activity (sports, running, strength training, or dancing).",
        "avoid": "Carbonated soft drinks, instant noodles, deep-fried street food, and heavy bakery items.",
        "days": {
            "Monday": {"Breakfast": "Ragi Java with mixed nuts & boiled sprouts.", "Lunch": "Bajra rotis with dal and leafy green stir-fry.", "Snack": "Roasted Chana.", "Dinner": "Millet pulao with curd raita."},
            "Tuesday": {"Breakfast": "Peanut butter whole wheat toast & banana.", "Lunch": "Brown rice, mixed vegetable sambar, and ivy gourd sabzi.", "Snack": "Boiled egg or sweet potato chat.", "Dinner": "Two chapatis with mixed vegetable curry."},
            "Wednesday": {"Breakfast": "Millet Poha with roasted peanuts.", "Lunch": "Jowar roti with green moong dal and beetroot salad.", "Snack": "Fruit salad with pumpkin seeds.", "Dinner": "Soya bean curry with brown rice."},
            "Thursday": {"Breakfast": "Oats omelette OR Moong dal chilla.", "Lunch": "Two whole wheat chapatis with chicken curry or paneer curry.", "Snack": "Thick buttermilk with cumin powder.", "Dinner": "Foxtail millet khichdi."},
            "Friday": {"Breakfast": "Ragi malt smoothie with almonds.", "Lunch": "Brown rice, spinach dal, and cluster beans sabzi.", "Snack": "Roasted makhana.", "Dinner": "Whole wheat pasta with lots of veggies & paneer."},
            "Saturday": {"Breakfast": "Sprouted chana salad with vegetable upma.", "Lunch": "Bajra roti with egg bhurji or thick chana masala.", "Snack": "Coconut water and a handful of walnuts.", "Dinner": "Jeera rice with dal fry."},
            "Sunday": {"Breakfast": "Multi-grain paneer paratha with curd.", "Lunch": "Millet biryani (veg/chicken) with cucumber raita.", "Snack": "A glass of milk with dry fruits.", "Dinner": "Light oats upma with vegetables."}
        }
    },
    "Adult (20-59)": {
        "sleep_ideal": "7 to 9 hours",
        "exercise": "30-45 minutes of moderate exercise 5 days a week (brisk walking, gym, yoga).",
        "avoid": "Excessive white sugar, refined flour (maida), highly processed packaged snacks, and late-night heavy meals.",
        "days": {
            "Monday": {"Breakfast": "Unsweetened Ragi Java with buttermilk & sprouts.", "Lunch": "Jowar Roti, a bowl of Toor Dal, and ladyfinger (bhindi) sabzi.", "Snack": "A handful of roasted chana.", "Dinner": "Light Foxtail Millet Khichdi with curd."},
            "Tuesday": {"Breakfast": "Millet Poha with roasted peanuts and lemon juice.", "Lunch": "Brown rice, mixed vegetable sambar, and palak stir-fry.", "Snack": "One seasonal fruit (Guava or Apple).", "Dinner": "Two whole wheat chapatis with paneer bhurji."},
            "Wednesday": {"Breakfast": "Oats Idli with mint and coriander chutney.", "Lunch": "Bajra Roti, green moong dal, and ivy gourd sabzi.", "Snack": "Plain buttermilk with roasted cumin powder.", "Dinner": "Broken wheat (dalia) upma with carrots and peas."},
            "Thursday": {"Breakfast": "Moong Dal Chilla (savory pancake) with curd.", "Lunch": "Jowar Roti, chana masala, and cucumber salad.", "Snack": "Soaked almonds and walnuts.", "Dinner": "Little Millet curd rice with a small side of stir-fried veggies."},
            "Friday": {"Breakfast": "Ragi porridge with a dash of jaggery and almonds.", "Lunch": "Brown rice, tomato rasam, and boiled egg or paneer curry.", "Snack": "Roasted makhana (foxnuts).", "Dinner": "Mixed vegetable clear soup with grilled tofu/paneer."},
            "Saturday": {"Breakfast": "Vegetable Upma made from multi-millet semolina.", "Lunch": "Whole wheat chapatis, ridge gourd curry, and dal.", "Snack": "Coconut water.", "Dinner": "Foxtail Millet pulao with raita."},
            "Sunday": {"Breakfast": "Healthy Multi-grain Dosa with ginger chutney.", "Lunch": "Brown rice or Jowar Roti, clean fish curry or sprouted methi dal.", "Snack": "A cup of green tea or spiced buttermilk.", "Dinner": "Light oats porridge or vegetable khichdi."}
        }
    },
    "Senior Citizen (60+)": {
        "sleep_ideal": "7 to 8 hours",
        "exercise": "20-30 minutes of low-impact movement (gentle walking, joint mobility stretches, light pranayama).",
        "avoid": "Hard-to-chew vegetables, heavily oiled pickles, high-sodium papads, and gas-forming heavy lentils.",
        "days": {
            "Monday": {"Breakfast": "Warm Ragi Ambali (porridge) with thin buttermilk.", "Lunch": "Soft-cooked rice, ridge gourd dal, and curd.", "Snack": "Stewed apple (soft).", "Dinner": "Thin vegetable khichdi (easy to digest)."},
            "Tuesday": {"Breakfast": "Soft oats porridge with milk.", "Lunch": "Mashed brown rice with bottle gourd (lauki) curry and moong dal.", "Snack": "Warm papaya pieces.", "Dinner": "Soft broken wheat dahlia upma."},
            "Wednesday": {"Breakfast": "Well-cooked idli with light tomato chutney.", "Lunch": "Soft jowar roti soaked in dal, with mashed ash gourd sabzi.", "Snack": "A cup of warm milk with turmeric.", "Dinner": "Clear vegetable broth with soft boiled paneer."},
            "Thursday": {"Breakfast": "Finger millet flour rava upma (very soft).", "Lunch": "Mashed rice, curd, and a side of soft boiled ivy gourd.", "Snack": "One ripe banana.", "Dinner": "Moong dal soup with an idli."},
            "Friday": {"Breakfast": "Warm ragi malt (sweet version with little jaggery).", "Lunch": "Soft rice, drumstick sambar, and mashed carrot subzi.", "Snack": "Thin curd water (lassi without ice).", "Dinner": "Oats porridge with no sugar, spices or oil."},
            "Saturday": {"Breakfast": "Soft-cooked vermicelli with carrots.", "Lunch": "Soft whole wheat chapati mashed inside yellow dal.", "Snack": "Stewed pear or warm papaya.", "Dinner": "Little millet khichdi cooked with extra water."},
            "Sunday": {"Breakfast": "Moong dal green chilla (soft texturized).", "Lunch": "Mashed rice, simple fish broth (if non-veg) OR light cumin flavored rasam and curd.", "Snack": "Coconut water.", "Dinner": "Warm vegetable stock soup with soft idli."}
        }
    }
}

CONDITION_ADVICE = {
    "None": "Keep maintaining a great, balanced health routine!",
    "Diabetes": "⚠️ *Diabetes Rule:* Avoid white sugar and refined white rice entirely. Substitute with Foxtail Millet or Jowar rotis. Prioritize high-fiber vegetables like okra, bitter gourd, and ivy gourd. Walk for 15 minutes immediately after meals.",
    "Hypertension (BP)": "⚠️ *Hypertension Rule:* Strictly limit table salt. Completely avoid commercial pickles, salted papads, frozen meals, and packed namkeens. Focus on potassium-rich options like coconut water, bottle gourd juice, and bananas.",
    "Gastric Issues / Acid Reflux": "⚠️ *Gastric Health Rule:* Avoid raw spices, red chili powder, coffee, and carbonated beverages. Do not leave long gaps between meals. Include cooling items like thin cold buttermilk, ash gourd juice, and well-cooked Ragi Ambali. Avoid heavy gas-forming lentils like whole rajma.",
    "Heart Health": "⚠️ *Cardiovascular Health Rule:* Eliminate deep-fried items, trans-fats, re-heated oils, and saturated fats (vanaspati/heavy butter). Focus on heart-healthy soluble fibers like oats and millets. Consume omega-3 choices like soaked walnuts and flaxseeds daily.",
    "Thyroid": "⚠️ *Thyroid Rule:* Avoid raw goitrogenic vegetables like uncooked cabbage, cauliflower, kale, and broccoli. Ensure adequate iodine/selenium from whole grains and soaked nuts. Focus on active weight management.",
    "Weight Loss": "⚠️ *Weight Loss Rule:* Maintain a structured calorie deficit. Drink 1 glass of *Ragi Java prepared with buttermilk* before your major meals to promote satiety. Swap heavy carb dinners out for clear vegetable soups or a light protein bowl."
}

# =========================================================================
# 2. CHATBOT RULES: DYNAMIC MULTI-KEYWORD LIFESTYLE ENGINE
# =========================================================================
EXTENDED_CHAT_RULES = {
    ("gastric", "acidity", "reflux", "gas", "bloating"): (
        "### 🤢 Managing Gastric Issues & Acid Reflux\n"
        "*🍛 Food Fix:* Drink cold buttermilk mixed with roasted cumin (jeera) powder. Include alkaline items like ash gourd juice or well-cooked Ragi Ambali. Avoid raw red chili powder, citrus fruits on an empty stomach, and heavy gas-forming lentils like whole rajma.\n\n"
        "*🏃‍♂️ Exercise Strategy:* Avoid bending or intense lifting immediately after eating. Practice Vajrasana (Adamantine Pose) for 5-10 minutes post-meals to assist intestinal motility.\n\n"
        "*⏰ Sleep Rule:* Sleep with your head elevated by 4-6 inches. Never lie flat within 2 hours of dinner to prevent stomach acid from washing up into the food pipe."
    ),
    ("heart", "bp", "hypertension", "cardiovascular", "cholesterol"): (
        "### 🫀 Cardiovascular Health & Pressure Balance\n"
        "*🍛 Food Fix:* Cut out processed snacks (packed namkeens, instant noodles) and heavy table salt. Replace refined white grains with high-fiber grains like oats, Jowar, and Foxtail Millets. Snack on 4-5 soaked almonds or walnuts for healthy fats.\n\n"
        "*🏃‍♂️ Exercise Strategy:* Aim for 30 minutes of brisk, steady cardio (walking, slow cycling) 5 days a week. Avoid sudden, explosive high-intensity weight strain if BP is unregulated.\n\n"
        "*⏰ Sleep Rule:* Ensure 7-8 hours of continuous rest. Chronic sleep deprivation spikes stress hormones like cortisol, forcing blood vessels to constrict and raising blood pressure."
    ),
    ("diabetes", "sugar", "glucose", "insulin"): (
        "### 🩸 Blood Glucose & Insulin Optimization\n"
        "*🍛 Food Fix:* Swap out high-glycemic carbohydrates like white rice or maida with Jowar rotis, Bajra, or broken brown dahlia. Prioritize high-fiber bitter vegetables (bitter gourd, okra, ivy gourd).\n\n"
        "*🏃‍♂️ Exercise Strategy:* Build muscle through resistance exercises or take a quick 15-minute steady walk immediately after lunch and dinner to clear glucose out of the blood stream.\n\n"
        "*⏰ Sleep Rule:* Poor sleep patterns create insulin resistance, making your body shift into a state where fat storage is prioritized and blood sugar fluctuates wildly."
    ),
    ("thyroid", "hypothyroid"): (
        "### 🦋 Thyroid Metabolic Regulation\n"
        "*🍛 Food Fix:* Avoid consuming raw, uncooked goitrogenic elements like cabbage, cauliflower, kale, or broccoli. Use whole grains, and ensure regular selenium and iodine from soaked nuts and seeds.\n\n"
        "*🏃‍♂️ Exercise Strategy:* Focus on active muscle mass restoration through moderate weight training and yoga poses like Sarvangasana to stimulate neck circulation.\n\n"
        "*⏰ Sleep Rule:* Maintain a strict circadian rhythm. Thyroid hormones align deeply with growth hormone production occurring during deep sleep states."
    ),
    ("weight loss", "lose weight", "dieting", "fat loss", "slim"): (
        "### 📉 Structured Weight Loss Engine\n"
        "*🔋 Core Strategy:* Create a clean, sustainable caloric deficit without skipping vital meals.\n\n"
        "*🥗 Food Tweaks:* Drink a warm glass of *Ragi Java prepared with thin buttermilk* 20 minutes before lunch or dinner. It keeps you full and stops overeating. Replace evening tea snacks with roasted makhana or cucumber salad.\n\n"
        "*🏃‍♂️ Exercise:* Combine full-body strength movements 3 times a week with daily steps (target 8,000 to 10,000 steps).\n\n"
        "*⚠️ Hidden Defect:* If you only sleep 5 hours, your body secretes more Ghrelin (the hunger hormone) and suppresses Leptin (the fullness signal), causing uncontrollable cravings for high-sugar foods."
    ),
    ("weight gain", "gain weight", "bulk", "muscle gain"): (
        "### 📈 Structured Weight & Muscle Gain Engine\n"
        "*🔋 Core Strategy:* Build healthy mass through a clean caloric surplus combined with lean muscle cultivation.\n\n"
        "*🥗 Food Tweaks:* Increase nutrient density instead of just eating junk food. Drink *Ragi malt mixed with whole milk*, jaggery, and crushed dry fruits twice a day. Incorporate paneer, sprouted chana, boiled eggs, and bananas into your daily routine.\n\n"
        "*🏃‍♂️ Exercise:* Focus on progressive resistance weight training (push-ups, squats, weighted movements) to ensure calories transform into lean muscle rather than simple fat deposits.\n\n"
        "*⏰ Sleep Factor:* Muscles heal and expand while you are sleeping! Target 8 solid hours for optimal growth hormone distribution."
    ),
    ("ragi", "finger millet", "java", "ambali"): (
        "### 🌾 Special Profile: Ragi (Finger Millet)\n"
        "* *Benefits:* Incredible plant-based source of calcium and iron. Exceptional for cooling your digestive system down and managing diabetes due to slow-digesting fibers.\n"
        "* *How to Prepare:* Eat it as thin Ragi Java with buttermilk for cooling/weight loss, or drink it thick with warm milk and a pinch of jaggery for weight gain/children's growth."
    ),
    ("millet", "millets", "jowar", "bajra", "foxtail"): (
        "### 🌾 Standard Millet Classifications\n"
        "Replacing white rice/refined flour with complex millets like *Jowar (Sorghum), **Bajra (Pearl Millet), or **Foxtail Millet* introduces rich magnesium and slow-release low-GI fuel. Always soak whole millets for 4-6 hours before boiling to break down anti-nutrients and ease stomach digestion."
    ),
    ("sleep", "insomnia", "tired", "fatigue", "night"): (
        "### 🌙 Sleep Framework Rules\n"
        "* *The Effect:* Restful sleep (7-9 hours) repairs tissue, flushes metabolic waste out of your brain, and balances metabolic speed.\n"
        "* *The Defect:* Missing sleep triggers high blood pressure, compromises immune defense, accelerates skin aging, and causes severe next-day mental fatigue and brain fog."
    ),
    ("exercise", "walking", "gym", "workout", "sitting", "sedentary"): (
        "### 🏃‍♂️ Physical Activity Parameters\n"
        "* *The Effect:* Daily activity enhances insulin receptivity, lowers bad cholesterol (LDL), protects your heart walls, and shoots feel-good endorphins into your system.\n"
        "* *The Defect:* Continuous prolonged sitting (sedentary behavior) slows blood flow, reduces bone density over time, decreases caloric expenditure, and causes lower back and hip stiffness."
    )
}

# =========================================================================
# 3. APPLICATION SETUP & LAYOUT TABS
# =========================================================================
st.set_page_config(page_title="Rule-Based Health AI Engine", page_icon="🤖", layout="wide")

st.title("🤖 Rule-Based Driven Health and Lifestyle Awareness AI Chatbot")
st.write("An automated rules engine analyzing age metrics, lifestyle routines, and health history parameters.")

# Creating Application Interface Tabs
tab1, tab2 = st.tabs(["📋 Personalized Lifestyle Assessment Form", "💬 Live Knowledge Chat Interface"])

# =========================================================================
# TAB 1: ASSESSMENT FORM & 7-DAY DIET MATRIX DISPLAY
# =========================================================================
with tab1:
    st.write("### 📝 Enter Personal Health Parameters")
    
    with st.form("health_assessment_form"):
        col1, col2 = st.columns(2)
        with col1:
            age_group = st.selectbox("👉 Select Your Age Group Bracket:", list(HEALTH_MATRIX.keys()))
            sleep_hours = st.number_input("👉 Enter Daily Sleep Hours:", min_value=1, max_value=24, value=7, step=1)
        with col2:
            health_issue = st.selectbox("👉 Select Underlying Primary Medical Concern:", list(CONDITION_ADVICE.keys()))
            routine = st.selectbox("👉 Select Daily Activity Routine Classification:", ["Sedentary (Sitting all day)", "Moderate Active", "Heavy Active"])
        
        submit_button = st.form_submit_button(label="⚡ Execute Rules & Compile 7-Day Plan")

    if submit_button:
        base_data = HEALTH_MATRIX[age_group]
        condition_data = CONDITION_ADVICE[health_issue]
        
        st.markdown("---")
        st.markdown("## 📋 Your Rule-Driven Health & Lifestyle Blueprint")
        
        # Sleep logic check
        sleep_comment = "✅ Your current sleep duration meets your age group criteria parameters."
        if "to" in base_data["sleep_ideal"]:
            ideal_min = int(base_data["sleep_ideal"].split()[0])
            if sleep_hours < ideal_min:
                sleep_comment = f"⚠️ Sleep Deficit Detected. Your profile target requires {base_data['sleep_ideal']}. Increase sleep duration."

        # Display Metrics Blocks
        st.info(f"*⏰ Sleep Evaluation Status:* {sleep_comment}")
        st.success(f"*🏃‍♂️ Prescribed Activity Matrix:* {base_data['exercise']}")
        st.warning(condition_data)
        
        st.markdown("### 🍛 Comprehensive 7-Day Diet Schedule")
        st.write(f"To maximize dietary consistency, follow this macro-balanced structural template optimized for *{age_group}* dynamics:")
        
        # Build tabular structured matrix display 
        table_data = []
        for day in WEEK_DAYS:
            meals = base_data["days"][day]
            table_data.append({
                "Day Order": day,
                "Breakfast Combo": meals["Breakfast"],
                "Lunch Core": meals["Lunch"],
                "Evening Snack Choice": meals["Snack"],
                "Dinner Option": meals["Dinner"]
            })
            
        st.table(table_data)
        st.error(f"🚫 *Strictly Avoid List:* {base_data['avoid']}")

# =========================================================================
# TAB 2: LIVE KNOWLEDGE CHAT INTERFACE
# =========================================================================
with tab2:
    st.write("### 💬 Automated Chat Bot Interrogator")
    st.caption("Ask specific health keyword metrics to parse advice (e.g., 'How to treat acidity?', 'Ragi benefits', 'Diabetes rules').")

    # Initializing local state for running conversations
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Print prior history blocks
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat execution engine logic
    if prompt := st.chat_input("Ask a nutrition or lifestyle query here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Baseline fallback fallback if search regex breaks
        bot_response = "🤖 I'm sorry, I couldn't map that specific phrase to a rule. Try terms like 'Gastric', 'BP', 'Diabetes', 'Thyroid', 'Millets', 'Sleep', or 'Weight Loss'."
        
        normalized_query = prompt.lower()
        
        # Scan dictionary tuples with a boundaries-safe regex search loop
        for key_tuple, descriptive_advice in EXTENDED_CHAT_RULES.items():
            if any(re.search(rf"\b{word}\b", normalized_query) for word in key_tuple):
                bot_response = descriptive_advice
                break
                
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
