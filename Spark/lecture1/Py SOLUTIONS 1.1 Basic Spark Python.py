# Databricks notebook source
# MAGIC %md 
# MAGIC #### ** Hey! Does this work? **

# COMMAND ----------

sc

# COMMAND ----------

1+1

# COMMAND ----------

# MAGIC %md
# MAGIC #### **Show the Spark Context**

# COMMAND ----------

dir(sc)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Some Basic Map/Reduce Operations

# COMMAND ----------

# filter, count, reduce
# define a function to map
n1 = sc.parallelize(range(1,1000)).map(lambda n: n if n%10==0 else None)
n2 = n1.filter(lambda n: n is not None)
n2.reduce(lambda x,y:x+y)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Calculate Pi

# COMMAND ----------

import random

NUM_SAMPLES=100000;

def myFunc(i):
  x=random.random()
  y=random.random()
  if x*x + y*y < 1:
    return 1
  return 0

count = sc.parallelize(range(NUM_SAMPLES)).map(myFunc).reduce(lambda x,y:x+y)

print("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))


# COMMAND ----------

# MAGIC %md
# MAGIC #### Setup S3 Credential And Mount S3 Bucket to Spark Cluster (Same for the whole course)
# MAGIC ### DO NOT CHECKIN to ANY PUBLIC GIT REPO

# COMMAND ----------

dbutils.fs.mount("s3a://"+"AKIAJH57T"+"SADMXPN"+"3NWA:cl7ON3wPVCf"+"a42eAzHjRD"+"v0iVJgsApuS"+"H3qwyMwF"+"@mlonspark", "/mnt/mlonspark")

# COMMAND ----------

# MAGIC %md
# MAGIC #### Open a File on S3 (All Titles of Wikinews)

# COMMAND ----------

myRDD = sc.textFile("/mnt/mlonspark/enwikinews-20160820-all-titles")

# COMMAND ----------

myRDD.take(10)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Count Total Number of Words

# COMMAND ----------

import re
p = re.compile(u'[^A-Za-z0-9_]+')
wordsRDD=myRDD.flatMap(lambda l: p.sub('',l).lower().split("_")).filter(lambda l: len(l)>0)
wordsRDD.count()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Word Count?

# COMMAND ----------

wordCountRDD = wordsRDD.map( lambda x: (str(x),1)).reduceByKey( lambda x,y: x+y )
wordCountRDD.take(5)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Find the most used 10 words

# COMMAND ----------

wordCountRDD.map( lambda x: (x[1], x[0])).sortByKey(False).take(10)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Drop stop words and try again

# COMMAND ----------

stopwords=set(["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]);

# COMMAND ----------

wordCountRDD.filter(lambda x: not x[0] in stopwords).filter(lambda x: len(x[0])>1).map( lambda x: (x[1], x[0])).sortByKey(False).take(10)

# COMMAND ----------

# MAGIC %md
# MAGIC ####Graph

# COMMAND ----------

rdd=sc.parallelize([('RUS',140),('GBR',64),('USA',314),('IND',1252),('CHN',1357)])
display(rdd.toDF())

# COMMAND ----------


