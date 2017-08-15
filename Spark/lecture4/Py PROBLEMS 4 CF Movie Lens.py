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



# COMMAND ----------

# MAGIC %md
# MAGIC #### Build the recommendation model using ALS
# MAGIC For simplicity, Use full dataset as training data

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC #### Evaluate the model by computing the RMSE on the test data

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC #### Now suggest top 5 items to user 194 (and print the movie names as well)
# MAGIC #####Hint: Play with SQL queries, show show something like (may not be exact):
# MAGIC #####| 601|For Whom the Bell...|  5.036547|
# MAGIC #####| 214|Pink Floyd - The ...|  4.898321|
# MAGIC #####| 713|      Othello (1995)|  4.778591|
# MAGIC #####|1073|Shallow Grave (1994)| 4.7152324|
# MAGIC #####|1059|Don't Be a Menace...|  4.685348|

# COMMAND ----------



# COMMAND ----------


