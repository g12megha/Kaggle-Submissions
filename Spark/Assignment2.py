# Databricks notebook source
# MAGIC %md
# MAGIC # Assignment Problem 2: Analyze Forest Coverage 

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Instructions 
# MAGIC **This is an Open-ended problem. I'm not looking for one correct answer, but an organized analysis report on the data. **
# MAGIC 
# MAGIC This is a very clean dataset great for classification. The data file contains 581,012 lines, each containing 55 fields. The first 54 fields are properties of a certain place on earth, the 55th field is the type of land coverage. Details of the fields in the README file below. 
# MAGIC 
# MAGIC 1. Use Spark to parse the file, prepare data for classification;
# MAGIC 1. Show some basic statistics of the data fields
# MAGIC 1. Build a Random Forest model in Spark to analyze the data. 
# MAGIC 1. Split the dataset to 70% and 30% for training and test dataset.  
# MAGIC 1. Train differnt classificiers and observe the performance/error rate of them. 
# MAGIC 1. Use Spark to do your calculations, then use dataframes to draw some plots. Describe each plot briefly and draw some conclusions.  

# COMMAND ----------

# MAGIC %md
# MAGIC #### How to work on and hand in this assignment
# MAGIC Write your analysis report, and send me the PDF of your Notebook before the assignment is due. 

# COMMAND ----------

# MAGIC %md
# MAGIC #### Load the data into an RDD

# COMMAND ----------

#read txt file, gzipped files will be auto-unzipped
myDataRDD = sc.textFile("/mnt/mlonspark/covtype.data.gz")
myReadmeRDD = sc.textFile("/mnt/mlonspark/covtype.info")

print myDataRDD.count()
myDataRDD.take(5)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Readme File

# COMMAND ----------

for l in myReadmeRDD.collect():
  print l
  

# COMMAND ----------


