# Rhino App API Documentation

This is a *stateless* API. As such, there is no database, nor user context that the API understands. It accepts a `session_id` 
parameter on many of the calls that the client stores. This represents the user to the API

## Interface

### GET /status

#### Returns
`'Up and working'`

### POST /status

#### Returns
`'Up and working'`

### GET /create_food_api_session

#### Parameters
* `uid` = user id *arbitrary string*
* `devid` = device id *arbitrary string*

#### Returns
`{'session_id': <SESSION_ID_FROM_FOOD_ESSENTIALS_API>}`

### POST /set_profile

#### Parameters
* `age` = 
* `height` = 
* `current_weight` = 
* `goal_weight` = 
* `weeks_to_goal` = 
* `gender` = 
* `activity_level` = 

All below are allergies, accept a boolean of `true` or `false`
* `cereal_allergy` = 
* `coconut_allergy` = 
* `corn_allergy` = 
* `egg_allergy` = 
* `fish_allergy` = 
* `gluten_allergy` = 
* `lactose_allergy` = 
* `milk_allergy` = 
* `peanuts_allergy` = 
* `sesame_seed_allergy` = 
* `shellfish_allergy` = 
* `soybean_allergy` = 
* `sulfites_allergy` = 
* `tree_nuts_allergy` = 
* `wheat_allergy` = 

#### Returns
`{'food_api_status': <FOOD_ESSENTIALS_API_STATUS_CODE>,
'daily_calorie_limit': <CALCULATED_DAILY_CALORIE_LIMIT_BASED_ON_WEIGHT_GOASL>}`

### GET /search

#### Parameters
* `upc` = 
* `session_id` = 

#### Returns
`{'item': <PRODUCT_NAME>,
'serving_size': <PRODUCT_SERVING_SIZE>,
'serving_size_uom': product['serving_size_uom'],
'servings_per_container': product['servings_per_container'],
'nutrients': [<NUTRIENTS>], 
'ingredients': <INGREDIENTS>,
'allergen_yellow_ingredients': allergen_yellow_ingredients,
'allergen_red_ingredients': allergen_red_ingredients,
'daily_calorie_limit': <CALCULATED_DAILY_CALORIE_LIMIT_BASED_ON_WEIGHT_GOASL>}`
