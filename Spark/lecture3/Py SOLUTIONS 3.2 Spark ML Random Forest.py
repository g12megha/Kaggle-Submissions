# Databricks notebook source
# MAGIC %md
# MAGIC # Spark ML
# MAGIC #### Dataset Introduction
# MAGIC This is a popular dataset for classification. Given a feature vector of 14 census results, the problem is to predict whether a persons income is greater than 50K. 

# COMMAND ----------

# MAGIC %md
# MAGIC #### Open Files (use traindata to train, testdata to test)

# COMMAND ----------

dbutils.fs.mount("s3a://"+"AKIAJH57T"+"SADMXPN"+"3NWA:cl7ON3wPVCf"+"a42eAzHjRD"+"v0iVJgsApuS"+"H3qwyMwF"+"@mlonspark", "/mnt/mlonspark")

# COMMAND ----------

# Import SQLContext and data types
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.ml import Pipeline
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import StringIndexer
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# sc is an existing SparkContext.
sqlContext = SQLContext(sc)


# COMMAND ----------

trainFileRDD = sc.textFile("/mnt/mlonspark/adult.traindata.gz")
testFileRDD = sc.textFile("/mnt/mlonspark/adult.testdata.gz")

trainFileRDD.take(10)

testFileRDD.take(10)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Description of Fields
# MAGIC Note: For all categorial data, the number the number corresponds to a category. I.e. 1 = "Private", 2="Self-emp-not-inc" for the workclass (2nd) column.
# MAGIC 
# MAGIC * 0-age: continuous.
# MAGIC * 1-workclass: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
# MAGIC * 2-fnlwgt: continuous.
# MAGIC * 3-education: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.
# MAGIC * 4-education-num: continuous.
# MAGIC * 5-marital-status: Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
# MAGIC * 6-occupation: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
# MAGIC * 7-relationship: Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
# MAGIC * 8-race: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
# MAGIC * 9-sex: Female, Male.
# MAGIC * 10-capital-gain: continuous.
# MAGIC * 11-capital-loss: continuous.
# MAGIC * 12-hours-per-week: continuous.
# MAGIC * 13-native-country: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.
# MAGIC * 14-income: >50K, <=50K

# COMMAND ----------

# MAGIC %md
# MAGIC #### Create a dataframe with the following fields matching the dataset:
# MAGIC With quotes: "age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"
# MAGIC 
# MAGIC Without Quotes: age ,  workclass ,  fnlwgt ,  education ,  education_num ,  marital_status ,  occupation ,  relationship ,  race ,  sex ,  capital_gain ,  capital_loss ,  hours_per_week ,  native_country ,  income 
# MAGIC 
# MAGIC (You'll find the above 2 lines useful when copy/pasting)

# COMMAND ----------

fields=["age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"]

a=trainFileRDD
b=a.map(lambda x:x.replace(" ","")) # remove all space
c=b.map(lambda x:x.split(",")) #split by ','
d=c.filter(lambda x:len(x)==15) #filter out bad lines with more/less fields
e=d.map(lambda x:[int(x[0]),x[1],int(x[2]),x[3],int(x[4]),x[5],x[6],x[7],x[8],x[9],int(x[10]),int(x[11]), int(x[12]), x[13],x[14]]) #convert number fields to number

trainDF=sqlContext.createDataFrame(e, fields)

a=testFileRDD
b=a.map(lambda x:x.replace(" ",""))
c=b.map(lambda x:x[:-1]) #remove the tailing '.' for test data, this is tricky :O
d=c.map(lambda x:x.split(","))
e=d.filter(lambda x:len(x)==15)
f=e.map(lambda x:[int(x[0]),x[1],int(x[2]),x[3],int(x[4]),x[5],x[6],x[7],x[8],x[9],int(x[10]),int(x[11]), int(x[12]), x[13],x[14]])

testDF=sqlContext.createDataFrame(f, fields)

trainDF.printSchema()


# COMMAND ----------

# MAGIC %md
# MAGIC #### Use StringIndexer to encode the "string" typed fields (i.e. generate the dataset we used in the Random Forest Section)
# MAGIC I.e. produce the following two dataframe objects:
# MAGIC * trainLFDF: is a dataframe of [features: list, label: ]
# MAGIC * testLFDF: is a dataframe of [features: list, label: int]
# MAGIC * where feactures is a list of double values, with all string values converted to double values
# MAGIC 
# MAGIC Hint: Create one StringIndexer object for each column to convert from String to double, then use a pipeline to add an array of StringIndexer objects
# MAGIC 
# MAGIC Use VectorAssembler
# MAGIC 
# MAGIC Look at here for example of StringIndexer: http://spark.apache.org/docs/latest/ml-features.html#stringindexer
# MAGIC 
# MAGIC Look at here for example of a Pipeline:
# MAGIC http://spark.apache.org/docs/latest/ml-guide.html#example-pipeline

# COMMAND ----------


workclassIndexer = StringIndexer().setInputCol("workclass").setOutputCol("workclassIndex")
educationIndexer = StringIndexer().setInputCol("education").setOutputCol("educationIndex")
marital_statusIndexer = StringIndexer().setInputCol("marital_status").setOutputCol("marital_statusIndex")
occupationIndexer = StringIndexer().setInputCol("occupation").setOutputCol("occupationIndex")
relationshipIndexer = StringIndexer().setInputCol("relationship").setOutputCol("relationshipIndex")
raceIndexer = StringIndexer().setInputCol("race").setOutputCol("raceIndex")
sexIndexer = StringIndexer().setInputCol("sex").setOutputCol("sexIndex")
native_countryIndexer = StringIndexer().setInputCol("native_country").setOutputCol("native_countryIndex")
incomeIndexer = StringIndexer().setInputCol("income").setOutputCol("incomeIndex")

featureAssembler = VectorAssembler()\
  .setInputCols(["age", "workclassIndex", "fnlwgt","educationIndex","education_num","marital_statusIndex","occupationIndex","relationshipIndex","raceIndex","sexIndex","capital_gain","capital_loss","hours_per_week","native_countryIndex"])\
  .setOutputCol("features")

convpipeline = Pipeline()\
  .setStages([workclassIndexer, educationIndexer, marital_statusIndexer, occupationIndexer, relationshipIndexer, raceIndexer, sexIndexer, native_countryIndexer, incomeIndexer, featureAssembler])

model = convpipeline.fit(trainDF)

trainLFDF = model.transform(trainDF).select("features", "incomeIndex")
testLFDF = model.transform(testDF).select("features", "incomeIndex")

#note that VectorAssembler will decide whether to use DenseVector or SparseVector for each row to save memory

testLFDF.take(10)

# COMMAND ----------

# MAGIC %md 
# MAGIC #### RandomForest
# MAGIC 1. Create another pipeline to train with training dataset RandomForestClassifier (with maxbins=50, numtrees=10, maxdepth=10).
# MAGIC 1. use the model to predict the test dataset
# MAGIC 1. use MulticlassClassificationEvaluator to get the "precision" of the model on the test dataset
# MAGIC 
# MAGIC example here: http://spark.apache.org/docs/latest/ml-ensembles.html#example-classification

# COMMAND ----------

# Train a RandomForest model.
rf = RandomForestClassifier()\
  .setLabelCol("incomeIndex")\
  .setFeaturesCol("features")\
  .setNumTrees(5)\
  .setMaxBins(50)\
  .setMaxDepth(3)\

rfpipeline = Pipeline()\
  .setStages([rf])

rfmodel=rfpipeline.fit(trainLFDF)

# Make predictions.
predictions = rfmodel.transform(testLFDF)


evaluator = MulticlassClassificationEvaluator()\
  .setLabelCol("incomeIndex")\
  .setPredictionCol("prediction")\
  .setMetricName("accuracy")
accuracy = evaluator.evaluate(predictions)

print "Test Error = %5.2f%%" % ((1.0 - accuracy)*100)

# COMMAND ----------


