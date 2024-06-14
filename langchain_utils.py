import pandas as pd
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

openai_api_key = "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"

def load_dataset():
    return pd.read_csv('diet_exercise_fitness.csv')

def generate_exercise_diet_plan(age, height_ft, weight_lbs, gym_days):
    
    height_cm = height_ft * 30.48  # 1 foot = 30.48 cm
    
    weight_kg = weight_lbs * 0.453592  # 1 pound = 0.453592 kg

    df = load_dataset()

    # Filter the dataset based on user input (Example: age, height, weight, and gym days)
    filtered_df = df[(df['age'] == age) & 
                     (df['height'] == height_cm) & 
                     (df['weight'] == weight_kg) & 
                     (df['gymtime'] == gym_days)]

    if filtered_df.empty:
        
        prompt_template = PromptTemplate(
            template=("Generate a personalized weekly exercise and diet plan based on the following parameters: "
                      "Age: {age}, Height: {height} cm, Weight: {weight} kg, Gym Days: {gym_days}. "
                      "The plan should include daily exercises and meals with emphasis on a balanced diet and fitness routine."),
            input_variables=["age", "height", "weight", "gym_days"]
        )
        llm = OpenAI(api_key=openai_api_key, temperature=0.7)
        chain = LLMChain(llm=llm, prompt=prompt_template)
        
        plan_input = {
            "age": age,
            "height": height_cm,
            "weight": weight_kg,
            "gym_days": gym_days
        }
        
        detailed_plan = chain.run(plan_input)
        exercises = detailed_plan.split('\n')
        exercises = [ex.strip() for ex in exercises if ex.strip()]  
        return exercises[:gym_days], {
            'meals': 3, 
            'fruit_meals': 1,  
            'veg_meals': 1,  
            'cooked_meals': 2  
        }, detailed_plan

    # Randomly select a plan 
    selected_plan = filtered_df.sample(n=1).iloc[0]

    # Use Langchain and OpenAI to generate a detailed exercise and diet plan
    prompt_template = PromptTemplate(
        template=("Based on the following data, generate a personalized weekly exercise and diet plan: "
                  "Age: {age}, Height: {height} cm, Weight: {weight} kg, Gym Days: {gym_days}, "
                  "Meals per day: {meal}, Fruit meals: {fruit_meals}, Vegetable meals: {veg_meals}, Cooked meals: {cooked_meals}."),
        input_variables=["age", "height", "weight", "gym_days", "meal", "fruit_meals", "veg_meals", "cooked_meals"]
    )
    llm = OpenAI(api_key=openai_api_key, temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt_template)

    exercise_plan = selected_plan['exercise']
    diet_plan = {
        'meals': selected_plan['meal'],
        'fruit_meals': selected_plan['fruit'],
        'veg_meals': selected_plan['veg'],
        'cooked_meals': selected_plan['cook']
    }

    plan_input = {
        "age": age,
        "height": height_cm,
        "weight": weight_kg,
        "gym_days": gym_days,
        "meal": diet_plan['meals'],
        "fruit_meals": diet_plan['fruit_meals'],
        "veg_meals": diet_plan['veg_meals'],
        "cooked_meals": diet_plan['cooked_meals']
    }

    detailed_plan = chain.run(plan_input)
    exercises = detailed_plan.split('\n')
    exercises = [ex.strip() for ex in exercises if ex.strip()]  
    
    return exercises[:gym_days], diet_plan, detailed_plan
