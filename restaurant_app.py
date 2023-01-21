from flask import Flask 
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
	return json.dumps(results_json)

@app.get('/get_restaurants_names/<city_name>')
def get_restaurant_names(city_name):
	query='''SELECT DISTINCT restaurant_id,restaurant_name,restaurant_address FROM top_foods_restaurants
	WHERE city=%s'''
	values=(city_name.lower(),)
	cursor.execute(query,values)
	#try:
	#	cursor.execute(query,values)
	#except:
	#	conn.rollback()
	#	return None
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
		restaurants.append(internal_dict)

	results_json['restaurants']=restaurants	
                 
	return json.dumps(results_json)

@app.get('/get_top_foods/<restaurant_id>')
def get_top_foods(restaurant_id):
	query='''SELECT food
	FROM 
	(SELECT *, DENSE_RANK() OVER (ORDER BY count DESC) AS rnk
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

	return json.dumps(results_json)

@app.get('/get_infodetails')
def get_info():
	results_json={}
	results_json['status']='succesful'
	results_json['cities']=1
	results_json['reviews']=int(2*10e6)
	results_json['restaurants']=5000

	return json.dumps(results_json)

