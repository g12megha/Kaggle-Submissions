# Databricks notebook source
# MAGIC %md
# MAGIC #### Setup S3 Credential (Same for the whole course, only need to do it once)

# COMMAND ----------

dbutils.fs.mount("s3a://"+"AKIAJH57T"+"SADMXPN"+"3NWA:cl7ON3wPVCf"+"a42eAzHjRD"+"v0iVJgsApuS"+"H3qwyMwF"+"@mlonspark", "/mnt/mlonspark")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Load file to RDD

# COMMAND ----------

import re
myLogRDD=sc.textFile("/mnt/mlonspark/NASA_access_log_Aug95").map(lambda l: map(''.join, re.findall(r'\"(.*?)\"|\[(.*?)\]|(\S+)', l))).filter(lambda l: len(l)==7)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Count total number of Lines

# COMMAND ----------

myLogRDD.count()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Print the first 10 lines

# COMMAND ----------

myLogRDD.take(10)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Print the first 10 lines where the method is POST

# COMMAND ----------

def doFilter(x):
  try:
    if x[4].split(' ')[0]=='POST':
      return True
  except:
    return  False

  return  False
    
myLogRDD.filter(doFilter).take(10)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Count the number of DISTINCT Requester Domain Name 

# COMMAND ----------

myLogRDD.map(lambda line: (line[0],1)).reduceByKey(lambda a,b:a+b).count()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Find the top 10 Requester 

# COMMAND ----------

myLogRDD.map(lambda line: (line[0],1)).reduceByKey(lambda a,b:a+b).map(lambda a:(a[1],a[0])).sortByKey(False).take(10)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Count the number of POST and GET log lines 

# COMMAND ----------

def doFilter(x):
  try:
    m=x[4].split(' ')[0]
    if m=='POST' or m=='GET':
      return True
  except:
    return  False
  return  False
    
myLogRDD.filter(doFilter).map(lambda x:(x[4].split(' ')[0],1)).reduceByKey(lambda a,b:a+b).take(10)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Find Distribution of Return Code

# COMMAND ----------

# MAGIC %md
# MAGIC Expected Output:
# MAGIC 
# MAGIC (1398987,200)
# MAGIC (134146,304)
# MAGIC (26497,302)
# MAGIC (10040,404)
# MAGIC (171,403)
# MAGIC (27,501)
# MAGIC (10,400)
# MAGIC (3,500)

# COMMAND ----------

retCodeCountRDD=myLogRDD.map(lambda x:(x[5],1)).reduceByKey(lambda a,b:a+b).map(lambda l:(l[1],l[0])).sortByKey(False)

retCodeCountRDD.collect()



# COMMAND ----------

# MAGIC %md
# MAGIC #### Draw the above distribution as bar charts

# COMMAND ----------

display(retCodeCountRDD.toDF())

# COMMAND ----------


