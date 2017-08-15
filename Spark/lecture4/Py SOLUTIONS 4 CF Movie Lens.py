# Databricks notebook source
# MAGIC %md
# MAGIC # Collaborative Filtering on 100K MovieLens Dataset

# COMMAND ----------

# MAGIC %md
# MAGIC #### Load data from S3 and Create RDDs

# COMMAND ----------

dbutils.fs.mount("s3a://"+"AKIAJH57T"+"SADMXPN"+"3NWA:cl7ON3wPVCf"+"a42eAzHjRD"+"v0iVJgsApuS"+"H3qwyMwF"+"@mlonspark", "/mnt/mlonspark")

# COMMAND ----------

ratingRDD = sc.textFile("/mnt/mlonspark/ml-100k/u.data")
itemRDD = sc.textFile("/mnt/mlonspark/ml-100k/u.item")
userRDD = sc.textFile("/mnt/mlonspark/ml-100k/u.user")
readmeRDD = sc.textFile("/mnt/mlonspark/ml-100k/README")

# COMMAND ----------

# MAGIC %md
# MAGIC #### Look at the README file to see what fields are in each file

# COMMAND ----------

readmeRDD.collect()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Import proper libraries

# COMMAND ----------

from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.ml import Pipeline
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.types import *
from pyspark.sql.functions import udf
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
import math

sqlContext = SQLContext.getOrCreate(sc)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Create DataFrame from data

# COMMAND ----------

ratingDF = sqlContext.createDataFrame(ratingRDD.map(lambda x:x.split("\t"))\
                                      .map(lambda x:(int(x[0]),int(x[1]),int(x[2]))),\
                                      ["user","item","rating"])
ratingDF.show()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Build the recommendation model using ALS
# MAGIC For simplicity, Use full dataset as training data

# COMMAND ----------

als = ALS(rank=20, maxIter=20, regParam=0.01, userCol="user", itemCol="item", ratingCol="rating")
model = als.fit(ratingDF)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Evaluate the model by computing the RMSE on the test data

# COMMAND ----------

# MAGIC %md
# MAGIC #### Method 1: Calculate directly using RMSE definition (Google it)

# COMMAND ----------

predictions = model.transform(ratingDF)

rmse = math.sqrt(predictions.rdd.filter(lambda x: not math.isnan(x.prediction) ).map(lambda x:(x.prediction-x.rating)*(x.prediction-x.rating)).mean())

print("Root-mean-square error = " + str(rmse))


# COMMAND ----------

# MAGIC %md
# MAGIC #### Method 2: use the spark build in RegressionEvaluator to do it
# MAGIC Need help of udf (user defined function) to massage dataFrame and filter non-NaN values. 

# COMMAND ----------



evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating",
                                predictionCol="prediction")

rmse = evaluator.evaluate(predictions)

print("Root-mean-square error = " + str(rmse))


# COMMAND ----------

# MAGIC %md
# MAGIC #### Now suggest top 5 items to user 194 (and print the movie names as well)
# MAGIC Hint: Play with SQL queries

# COMMAND ----------

userid=194

ratingDF.createOrReplaceTempView("rating")

#Movies rated by this user
ratedbyuserDF=spark.sql('SELECT DISTINCT item FROM rating WHERE user = %d'%userid)
ratedbyuserDF.createOrReplaceTempView("ratedbyuser")
print ratedbyuserDF.count()
ratedbyuserDF.show()

#Movies not rated by this user (make it a tuple of user,item)
toberatedDF=spark.sql('SELECT DISTINCT %d as user, item FROM rating WHERE item not in (select item from ratedbyuser)'%userid)
print toberatedDF.count()
toberatedDF.show()

# COMMAND ----------

#Make predictions
predictedRatingDF=model.transform(toberatedDF)
predictedRatingDF.show()

# COMMAND ----------

#get the highest 5 predictions
predictedRatingDF.createOrReplaceTempView("predictedRating")
highest5DF=spark.sql('SELECT item, prediction from predictedRating order by prediction desc limit 5')

highest5DF.createOrReplaceTempView("high5predictedRating")
highest5DF.show()

# COMMAND ----------

#Now let's find out the name of these items

#create a DF for item->itemName mapping
nameofitemDF = sqlContext.createDataFrame(itemRDD.map(lambda x:x.split("|"))\
                                    .map(lambda x:(int(x[0]),x[1].encode('ascii','ignore'))),\
                                    ["item","itemName"])
nameofitemDF.createOrReplaceTempView("nameofitem")

#use SQL JOIN operation
highest5nameDF=spark.sql('SELECT a.item, b.itemName, a.prediction from high5predictedRating as a join nameofitem as b on a.item = b.item order by a.prediction desc')

highest5nameDF.show()


# COMMAND ----------


