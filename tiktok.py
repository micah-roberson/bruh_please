import pandas as pd 
from sqlalchemy import create_engine
df = pd.read_csv("meal_plans_20k copy.csv", encoding='latin-1')
print(df.head)
print(df.columns)
connection_string = 'postgresql://clevercart:password1234@clevercart-app.cfmc8shzhut6.us-east-2.rds.amazonaws.com/einstein'
engine = create_engine(connection_string)
table_name = 'meal_plan_20k'
df.to_sql(table_name, engine, if_exists='replace', index=False)