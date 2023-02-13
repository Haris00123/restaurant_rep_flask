from flask import Flask,jsonify,request
import psycopg2
import json

app=Flask(__name__)

conn=psycopg2.connect(
host='db-postgresql-tor1-38542-do-user-13162346-0.b.db.ondigitalocean.com',
database='restaurant_rep',
port=25060,
user='doadmin',
password='AVNS_YKtI3cC827SO2M3fZ12'
)

cursor=conn.cursor()

@app.route('/')
def hello():
	return 'hello, world!'

@app.get('/get_cities')
def get_curr_cities():
	query='''SELECT DISTINCT(city) FROM restaurants_list'''
	
	try:
		cursor.execute(query)
	except:
		conn.rollbac()
		return None
	returns=cursor.fetchall()

	results_json={}
    	
	if len(returns)>0:
		results_json['status']='succesful'
	else:
		results_json['status']='unsuccesful'
	
	return_count=len(returns)
	results_json['number_cities']=return_count
	cities=[]

	for i,c in enumerate(returns):
		internal_dict={}
		internal_dict['id']=i
		internal_dict['city_name']=c[0].capitalize()
		cities.append(internal_dict)
	results_json['cities']=cities
	response=jsonify(results_json)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

# @app.get('/get_restaurants_names/<city_name>')
# def get_restaurant_names(city_name):
# 	query='''SELECT DISTINCT restaurant_id,restaurant_name,restaurant_address FROM top_foods
# 	WHERE city = %s'''
# 	values=(city_name.lower(),)
# 	#cursor.execute(query,values)
# 	try:
# 		cursor.execute(query,values)
# 	except:
# 		conn.rollback()
# 		return None
# 	returns=cursor.fetchall()
	
# 	results_json={}

# 	if len(returns)>0:
# 		results_json['status']='succesful'
# 	else:
# 		results_json['status']='unsuccesful'
	
# 	return_count=len(returns)
# 	results_json['restaurant_count']=return_count
# 	restaurants=[]

# 	for r in returns:
# 		internal_dict={}
# 		internal_dict['id']=r[0]
# 		internal_dict['restaurant_name']=r[1].capitalize()
# 		internal_dict['restaurant_address']=r[2]
# 		restaurants.append(internal_dict)

# 	results_json['restaurants']=restaurants	
# 	response=jsonify(results_json)
# 	response.headers.add('Access-Control-Allow-Origin', '*')
# 	return response

@app.get('/get_restaurants_names')
def get_restaurant_names():
	res_name=request.args.get('resName')
	res_city=request.args.get('resCity')
	query='''SELECT * FROM top_foods_restaurants
			WHERE SIMILARITY(restaurant_name,%s)>0.3
			AND city=%s;'''
	values=(res_name.lower(),res_city.lower())
	#cursor.execute(query,values)
	try:
		cursor.execute(query,values)
	except:
		conn.rollback()
		return None
	returns=cursor.fetchall()
	
	results_json={}

	if len(returns)>0:
		results_json['status']='succesful'
	else:
		results_json['status']='unsuccesful'
	
	return_count=len(returns)
	results_json['restaurant_count']=return_count
	restaurants=[]

	for r in returns:
		internal_dict={}
		internal_dict['id']=r[0]
		internal_dict['restaurant_name']=r[1].capitalize()
		internal_dict['restaurant_address']=r[2]
		internal_dict['restaurant_city']=r[3]
		restaurants.append(internal_dict)

	results_json['restaurants']=restaurants	
	response=jsonify(results_json)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.get('/search_top_food')
def get_restaurants_by_food():
	food=request.args.get('Food')
	res_city=request.args.get('resCity')
	query='''SELECT restaurant_id,restaurant_name,restaurant_address,food  
			FROM
				(SELECT *, 
				RANK() OVER (PARTITION BY restaurant_address ORDER BY score DESC) AS rn
				FROM
					(SELECT restaurant_id,restaurant_name,restaurant_address,food,score
					FROM top_foods
					WHERE SIMILARITY(food,%s)>0.5 AND city = %s
					ORDER BY score DESC
					LIMIT 100) AS tmp) AS tmp_2
			WHERE rn=1
			ORDER BY score DESC
			LIMIT 10;
'''
	values=(food.lower(),res_city.lower())
	#cursor.execute(query,values)
	try:
		cursor.execute(query,values)
	except:
		conn.rollback()
		return None
	returns=cursor.fetchall()
	
	results_json={}

	if len(returns)>0:
		results_json['status']='succesful'
	else:
		results_json['status']='unsuccesful'
	
	return_count=len(returns)
	results_json['restaurant_count']=return_count
	restaurants=[]

	for i,r in enumerate(returns):
		internal_dict={}
		internal_dict['id']=r[0]
		internal_dict['rank']=i+1
		internal_dict['restaurant_name']=r[1].capitalize()
		internal_dict['restaurant_address']=r[2]
		internal_dict['food']=r[3]
		restaurants.append(internal_dict)

	results_json['restaurants']=restaurants	
	response=jsonify(results_json)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.get('/get_top_foods')
def get_top_foods():
	restaurant_id=request.args.get('resId')
	query='''SELECT food
	FROM 
	(SELECT *, DENSE_RANK() OVER (ORDER BY score DESC) AS rnk
	FROM top_foods
	WHERE restaurant_id=%s) AS tmp
	WHERE rnk<=5'''
	values=(restaurant_id,)
	try:
		cursor.execute(query,values)
	except:
		conn.rollback()
		return None

	returns=cursor.fetchall()
	
	results_json={}

	if len(returns)>0:
		results_json['status']='succesful'
	else:
		results_json['status']='unsuccesful'
	
	top_foods=[]

	for i,c in enumerate(returns):
		internal_dict={}
		internal_dict['id']=i
		internal_dict['rank']=i+1
		internal_dict['food']=c[0]
		top_foods.append(internal_dict)
	
	results_json['top_foods']=top_foods

	response=jsonify(results_json)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.get('/get_infodetails')
def get_info():
	results_json={}
	results_json['status']='succesful'
	results_json['cities']=2
	results_json['reviews']=int(4*10e6)
	results_json['restaurants']=10000

	response=jsonify(results_json)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__=="__main__":
	app.run()
