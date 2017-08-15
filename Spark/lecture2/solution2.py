    # Databricks notebook source
# MAGIC %md
# MAGIC # Play with Stars observed by a real Telescope
# MAGIC Note: real astronomy may do similar things

# COMMAND ----------

# MAGIC %md
# MAGIC #### Setup S3 Credential (Same for the whole course, only need to do it once)

# COMMAND ----------

dbutils.fs.mount("s3a://"+"AKIAJH57T"+"SADMXPN"+"3NWA:cl7ON3wPVCf"+"a42eAzHjRD"+"v0iVJgsApuS"+"H3qwyMwF"+"@mlonspark", "/mnt/mlonspark")

# COMMAND ----------

# MAGIC %md
# MAGIC #### Load Data and Turn the input data into an RDD of 5-tuples. 
# MAGIC Each Tuple should be like (ID, X, Y, Magnitude, SomethingElse)

# COMMAND ----------

#The data look like the following:
# 69068950,308.119646267,35.4419336308,19.7586,18.2142
# 71078341,349.28343638,54.5848277797,18.4068,17.6605
# 71450647,355.444119504,43.6987423493,21.6972,20.3539

# It is a CSV file, each line have 5 values, they are (with type):
# ID    ,      X,      Y, Magnitude, SomeThingElse
# String, double, double, double   , double

from pyspark.sql.types import *

myRDD = sc.textFile("/mnt/mlonspark/sdss.txt")
tuples = myRDD.map(lambda x:x.split(",")) \
.map(lambda x:(str(x[0]),float(x[1]), float(x[2]),float(x[3]),float(x[4]))) 

tuples.take(3)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Draw where all the stars are in a 2D map
# MAGIC Hint: convert to DF

# COMMAND ----------

# The schema is encoded in a string.
schemaString = "X Y"

fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)

# Apply the schema to the RDD.
myDF = spark.createDataFrame(tuples.map(lambda x:(x[1],x[2])), schema)

display(myDF)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Find min/max value of magnitude

# COMMAND ----------

mmin=tuples.map(lambda x:x[3]).min()
mmax=tuples.map(lambda x:x[3]).max()

print mmin, mmax

# COMMAND ----------

# MAGIC %md
# MAGIC #### Use O(n) time to get the brightest Star (i.e. smallest Magnitude), and return all info about that star
# MAGIC Hint: Use reduce

# COMMAND ----------

tuples.reduce(lambda t1,t2:t1 if(t1[3]<t2[3]) else t2)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Use "bar chat" to Draw a histogram of Magnitude, bin to Integers from 12 to 30
# MAGIC i.e. if a star's magnitude is 12.65, put it into the bin 12. 
# MAGIC TRY NOT TO USE THE "HISTOGRAM" PLOT

# COMMAND ----------


# The schema is encoded in a string.
schemaString = "Magnitude Count"

fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)

# Apply the schema to the RDD.
myDF = spark.createDataFrame(tuples \
                             .map(lambda t:(int(t[3]),1)) \
                             .reduceByKey(lambda x,y:x+y) \
                             .sortByKey(), schema)

display(myDF)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Find the pair of stars that are the farthest away from each other
# MAGIC (Assume the distance between two stars is sqrt((X1-X2)^2+(Y1-Y2)^2))
# MAGIC 
# MAGIC Hint, use cartisian to make a "self-crossjoin"

# COMMAND ----------

from math import sqrt
ct=tuples \
.map(lambda t:(t[0],t[1],t[2])) \
.cartesian( \
           tuples.map(lambda t:(t[0],t[1],t[2])) \
          ) \
.map(lambda s:(s[0][0], s[1][0], sqrt((s[0][1]-s[1][1])*(s[0][1]-s[1][1])+(s[0][2]-s[1][2])*(s[0][2]-s[1][2])))) \
.reduce(lambda s1,s2: s1 if s1[2]>s2[2] else s2)
print ct

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Find the star with the most number of neighbors within radius R. 
# MAGIC I.e. For each star, draw a circle of radius R around it, then count how many stars are in the circle, then do a max. 
# MAGIC 
# MAGIC Result is: Star ID=168138483 has 14 neighbours within Radius 10 
# MAGIC 
# MAGIC Note: Make sure not to clount itself as a neighbour

# COMMAND ----------

R=10.0
mm=tuples \
.map(lambda t:(t[0],t[1],t[2])) \
.cartesian( \
           tuples.map(lambda t:(t[0],t[1],t[2])) \
          ) \
.map(lambda s: \
     (s[0][0], 1) \
     if s[0][0]!=s[1][0] and sqrt((s[0][1]-s[1][1])*(s[0][1]-s[1][1])+(s[0][2]-s[1][2])*(s[0][2]-s[1][2]))<R \
     else \
     (s[0][0],0)) \
.reduceByKey(lambda x,y: x+y) \
.map(lambda s: (s[1],s[0])) \
.sortByKey(False) \
.take(12)

print mm

# COMMAND ----------


