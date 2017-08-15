# Databricks notebook source
# MAGIC %md
# MAGIC # Spark ML Pipeline Demo

# COMMAND ----------

# Import SQLContext and data types
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.ml import Pipeline
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.classification import LogisticRegression

# sc is an existing SparkContext.
sqlContext = SQLContext(sc)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Make a Training Set 

# COMMAND ----------

# Prepare training data from a list of (id, text, label) tuples.
training = sqlContext.createDataFrame([\
  (0, "a b c d e spark", 1.0),\
  (1, "b d", 0.0),\
  (2, "spark f g h", 1.0),\
  (3, "hadoop mapreduce", 0.0),\
  (4, "b spark who", 1.0),\
  (5, "g d a y", 0.0),\
  (6, "spark fly", 1.0),\
  (7, "was mapreduce", 0.0),\
  (8, "e spark program", 1.0),\
  (9, "a e c l", 0.0),\
  (10, "spark compile", 1.0),\
  (11, "hadoop software", 0.0)], ["id", "text", "label"])
training.show()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Simple Pipeline with "Tokenizer" as a Transformer

# COMMAND ----------

# Configure an ML pipeline, which consists of 1 stage: tokenizer
tokenizer = Tokenizer()\
  .setInputCol("text")\
  .setOutputCol("words")\

  
pipeline = Pipeline()\
  .setStages([tokenizer])

cvModel = pipeline.fit(None)

cvModel.transform(training).show()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Pipeline with Tokenizer and HashingTF(Feature Generation)

# COMMAND ----------

hashingTF = HashingTF()\
  .setInputCol(tokenizer.getOutputCol())\
  .setOutputCol("features")\

pipeline = Pipeline()\
  .setStages([tokenizer, hashingTF])\

cvModel = pipeline.fit(None)

cvModel.transform(training).show()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Pipeline with Tokenizer, HashingTF(Feature Generation) and Logistic Regression

# COMMAND ----------

lr = LogisticRegression()\
  .setMaxIter(10)

pipeline = Pipeline()\
  .setStages([tokenizer, hashingTF, lr])

cvModel = pipeline.fit(training)

cvModel.transform(training).select("text","label","prediction").show()


# COMMAND ----------

# MAGIC %md
# MAGIC ## String Indexer Example

# COMMAND ----------

from pyspark.ml.feature import StringIndexer

df = spark.createDataFrame(
    [(0, "a"), (1, "b"), (2, "c"), (3, "a"), (4, "a"), (5, "c")],
    ["id", "category"])

indexer = StringIndexer(inputCol="category", outputCol="categoryIndex")
indexed = indexer.fit(df).transform(df)
indexed.show()


# COMMAND ----------


