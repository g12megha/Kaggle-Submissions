# Databricks notebook source
# MAGIC %md
# MAGIC # Clustering 100K MovieLens Dataset

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
# MAGIC #### Import proper libraries

# COMMAND ----------

from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.ml import Pipeline
from pyspark.ml.recommendation import ALS
from pyspark.ml.clustering import KMeans

from pyspark.ml.linalg import Vector, VectorUDT, DenseVector

sqlContext = SQLContext.getOrCreate(sc)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Create a ALS model as done in previous section
# MAGIC Use Rank=2 to simplify KMeans visualization in the following steps (In real world use more Rank)

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC #### Extract itemFactors for clustering
# MAGIC Use model.itemFactors.rdd as a starting point to make a DataFrame of DenseVector out of it. 

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC #### Fit a K-Means model with K=5

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC #### Visualize the Data Points on a 2D Scatter Plot 
# MAGIC Color code them according to cluster id, and see if the cluster make sense

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC #### Evaluate clustering by computing Within Set Sum of Squared Errors

# COMMAND ----------


