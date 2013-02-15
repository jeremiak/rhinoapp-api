from datetime import datetime
from os import environ

from bottle import get, post, redirect, request, response, run
import requests
import simplejson as json

FOOD_API = 'http://api.foodessentials.com/%s'
MASHERY_KEY = environ.get('MASHERY_KEY')

def get_food_label(upc, session_id):
    params = {}
    params['u'] = upc
    params['sid'] = session_id
    r = requests.get((FOOD_API % 'labelarray'), params=params, data={'api_key': MASHERY_KEY})

    return r.json()

def calculate_nutrient_percents(nutrients, daily_cal):
    daily_allowance = {}
    daily_allowance['Total Fat'] = 0.0325 * daily_cal
    daily_allowance['Saturated Fat'] = 0.01 * daily_cal
    daily_allowance['Cholesterol'] = 0.15 * daily_cal
    daily_allowance['Sodium'] = 1.2 * daily_cal
    daily_allowance['Potassium'] = 1.75 * daily_cal
    daily_allowance['Total Carbohydrate'] = .15 * daily_cal
    daily_allowance['Sugars'] = 0.02 * daily_cal
    daily_allowance['Fiber'] = 0.0125 * daily_cal
    daily_allowance['Protein'] = 0.025 * daily_cal
    daily_allowance['Vitamin A'] = 2.5 * daily_cal
    daily_allowance['Vitamin C'] = 0.03 * daily_cal
    daily_allowance['Calcium'] = 0.5 * daily_cal
    daily_allowance['Iron'] = 0.009 * daily_cal

    data = {}
    for nutrient in nutrients:
        name = nutrient['nutrient_name']
        if name != 'Calories':
            if daily_allowance.get(name, None) != None:
                if nutrient['nutrient_value'] == '' or nutrient['nutrient_value'] == '0.0':
                    value = 0
                else:
                    value = int(float(nutrient['nutrient_value']))
                
                uom = nutrient['nutrient_uom']
                percentage = value/daily_allowance[name] * 100
                
                data[name] = {'Value': int(value),
                        'uom': uom,
                        'Percent': ('%d' % percentage + '%')}
        else:
            data['Calories'] = {'Value': int(float(nutrient['nutrient_value']))}
    return data

def calculate_daily_intake(age, height, current_weight, goal_weight, weeks_to_goal, gender, activity_level):
    pounds_per_week = (current_weight - goal_weight) / weeks_to_goal

    if gender == 'male':
        bmr = 66 + (6.3 * current_weight) + (12.9 * height) - (6.8 * age)
    else:
        bmr = 655 + (4.3 * current_weight) + (4.7 * height) - (4.7 * age)

    if activity_level == 'sedentary':
        bmr_and_activity = 1.2 * bmr
    elif activity_level == 'lightly active':
        bmr_and_activity = 1.3 * bmr
    elif activity_level == 'moderately active':
        bmr_and_activity = 1.4 * bmr
    elif activity_level == 'very active':
        bmr_and_activity = 1.5 * bmr
    
    limit = bmr_and_activity - ((pounds_per_week * 3500) / 7)

    return limit

@get('/search')
def search_upc():
    response.headers['Access-Control-Allow-Origin'] = '*'

    for param in request.query.keys():
        print "%s: %s" % (param, request.query.get(param))

    upc = request.query.get('upc', '016000264601')
    session_id = request.query.get('session_id')
    daily_calorie_limit = float(request.query.get('daily_cal', '2000'))

    label = get_food_label(upc, session_id)
    product = label['productsArray'][0]
    nutrients = calculate_nutrient_percents(product['nutrients'], daily_calorie_limit)
    
    data = {'item': product['product_name'],
            'serving_size': product['serving_size'],
            'serving_size_uom': product['serving_size_uom'],
            'servings_per_container': product['servings_per_container'],
            'nutrients': nutrients, 
            'ingredients': product['ingredients'],
            'daily_calorie_limit': daily_calorie_limit}

    return data

@post('/set_profile')
def set_profile():
    response.headers['Access-Control-Allow-Origin'] = '*'

    age = int(request.forms.get('age', '25'))
    height = int(request.forms.get('height', '70'))
    current_weight = int(request.forms.get('current_weight', '180'))
    goal_weight = int(request.forms.get('goal_weight', '170'))
    weeks_to_goal = int(request.forms.get('weeks_to_goal', '4'))
    gender = request.forms.get('gender', 'male').lower()
    activity_level = request.forms.get('activity_level', 'sedentary').lower()

    daily_calorie_limit = calculate_daily_intake(age, height, current_weight, goal_weight, weeks_to_goal, gender, activity_level)

    true_nutrients = ['Calcium', 'Calories', 'Calories from Fat', 'Cholesterol', 'Dietary Fiber', 'Insoluble Fiber', 'Iron',
            'Monounsaturated Fat', 'Other Carbohydrate', 'Polyunsaturated Fat', 'Potassium', 'Protein', 'Saturated Fat',
            'Saturated Fat Calories', 'Sodium', 'Soluble Fiber', 'Sugar Alcohol', 'Sugars', 'Total Carbohydrate',
            'Total Fat', 'Vitamin A', 'Vitamin C']

    nutrients = []
    for nutrient in true_nutrients:
        n = {'name': nutrient, 'value': 'true'}
        nutrients.append(n)
    
    session_id = request.forms.get('session_id', None)

    cereal_allergy = request.forms.get('cereal_allergy', 'false')
    coconut_allergy = request.forms.get('coconut_allergy', 'false')
    corn_allergy = request.forms.get('corn_allergy', 'false')
    egg_allergy = request.forms.get('egg_allergy', 'false')
    fish_allergy = request.forms.get('fish_allergy', 'false')
    gluten_allergy = request.forms.get('gluten_allergy', 'false')
    lactose_allergy = request.forms.get('lactose_allergy', 'false')
    milk_allergy = request.forms.get('milk_allergy', 'false')
    peanuts_allergy = request.forms.get('peanuts_allergy', 'false')
    sesame_seed_allergy = request.forms.get('sesame_seed_allergy', 'false')
    shellfish_allergy = request.forms.get('shellfish_allergy', 'false')
    soybean_allergy = request.forms.get('soybean_allergy', 'false')
    sulfites_allergy = request.forms.get('sulfites_allergy', 'false')
    tree_nuts_allergy = request.forms.get('tree_nuts_allergy', 'false')
    wheat_allergy = request.forms.get('wheat_allergy', 'false')
  
    allergens=  [{"name": "Cereals","value": cereal_allergy},
            {"name": "Coconut","value": coconut_allergy},
            {"name": "Corn","value": corn_allergy},
            {"name": "Egg","value": egg_allergy}, 
            {"name": "Fish","value": fish_allergy},
            {"name": "Gluten","value": gluten_allergy},
            {"name": "Lactose","value": lactose_allergy},
            {"name": "Milk","value": milk_allergy},
            {"name": "Peanuts","value": peanuts_allergy},
            {"name": "Sesame Seeds","value": sesame_seed_allergy},
            {"name": "Shellfish","value": shellfish_allergy},
            {"name": "Soybean","value": soybean_allergy},
            {"name": "Sulfites","value": sulfites_allergy},
            {"name": "Tree Nuts","value": tree_nuts_allergy},
            {"name": "Wheat","value": wheat_allergy}]

    additives = [{"name": "Acidity Regulator","value": "false"},
            {"name": "Added Sugar","value": "false"},
            {"name": "Anti-Caking Agents","value": "false"},
            {"name": "Anti-Foaming Agent","value": "false"},
            {"name": "Antioxidants","value": "false"},
            {"name": "Artificial Color","value": "false"},
            {"name": "Artificial Flavoring Agent","value": "false"},
            {"name": "Artificial Preservative","value": "false"},
            {"name": "Bulking Agents","value": "false"},
            {"name": "Colors","value": "false"},
            {"name": "Emulsifiers","value": "false"},
            {"name": "Enzyme","value": "false"},
            {"name": "Firming Agent","value": "false"},
            {"name": "Flavor Enhancer","value": "false"},
            {"name": "Flour Treating Agent","value": "false"},
            {"name": "Food Acids","value": "false"},
            {"name": "Gelling Agents","value": "false"},
            {"name": "Glazing Agent","value": "false"},
            {"name": "Humectants","value": "false"},
            {"name": "Leavening Agent","value": "false"},
            {"name": "Mineral Salt","value": "false"},
            {"name": "Natural Color","value": "false"},
            {"name": "Natural Flavoring Agent","value": "false"},
            {"name": "Natural Preservative","value": "false"},
            {"name": "Preservatives","value": "false"},
            {"name": "Propellant","value": "false"},
            {"name": "Raising Agents","value": "false"},
            {"name": "Saturated Fat","value": "false"},
            {"name": "Sequestrant","value": "false"},
            {"name": "Stabilizers","value": "false"},
            {"name": "Sweeteners","value": "false"},
            {"name": "Thickeners","value": "false"},
            {"name": "Trans Fat","value": "false"},
            {"name": "Unsaturated Fat","value": "false"},
            {"name": "Vegetable Gum","value": "false"}]

    params = {'sid': session_id, 'nutrients': nutrients, 'allergens': allergens, 'additives': additives, 'myingredients': [], 'mysort': []}

    r = requests.post((FOOD_API % 'setprofile'), params=json.dumps({'json': params}), data={'api_key': MASHERY_KEY})

    return {'food_api_status': r.status_code, 'daily_calorie_limit': daily_calorie_limit}

@get('/create_food_api_session')
def create_session():
    response.headers['Access-Control-Allow-Origin'] = '*'

    uid = request.query.get('uid', 'rhino_user')
    devid = request.query.get('devid', 'rhino_device')

    params = {}
    params['uid'] = uid
    params['devid'] = devid
    params['api_key'] = MASHERY_KEY
    params['f'] = 'json'

    r = requests.get((FOOD_API % 'createsession'), params=params)

    session_id = r.json().get('session_id', None)
    
    return session_id

@get('/status')
@post('/status')
def return_status():
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    for param in request.query.keys():
        print "%s: %s" % (param, request.query.get(param))

    return "Up and working"

run(host="0.0.0.0", port=int(environ.get("PORT", 5000)), reloader=True)
