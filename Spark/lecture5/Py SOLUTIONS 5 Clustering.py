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

ratingDF = sqlContext.createDataFrame(ratingRDD.map(lambda x:x.split("\t"))\
                                      .map(lambda x:(int(x[0]),int(x[1]),int(x[2]))),\
                                      ["user","item","rating"])
als = ALS(rank=2, maxIter=20, regParam=0.01, userCol="user", itemCol="item", ratingCol="rating")
model = als.fit(ratingDF)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Extract itemFactors for clustering
# MAGIC Use model.itemFactors.rdd as a starting point to make a DataFrame of DenseVector out of it. 

# COMMAND ----------

df=sqlContext.createDataFrame(model.itemFactors.rdd.map(lambda x: (x.id, DenseVector(x.features))),
                              ["id","features"])
df.show()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Fit a K-Means model with K=5

# COMMAND ----------

kmeans = KMeans().setK(5).setSeed(1)
model = kmeans.fit(df)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Visualize the Data Points on a 2D Scatter Plot 
# MAGIC Color code them according to cluster id, and see if the cluster make sense

# COMMAND ----------

clusteredDF=model.transform(df)
display(sqlContext.createDataFrame(clusteredDF.rdd.map(lambda x: (x.prediction,x.features.toArray())).map(lambda x:(x[0],float(x[1][0]), float(x[1][1])))))


# COMMAND ----------

# MAGIC %md
# MAGIC #### Evaluate clustering by computing Within Set Sum of Squared Errors

# COMMAND ----------


wssse = model.computeCost(df)
print("Within Set Sum of Squared Errors = " + str(wssse))

centers = model.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)


# COMMAND ----------


