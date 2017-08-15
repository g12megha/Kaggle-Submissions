# Databricks notebook source
# MAGIC %md
# MAGIC # Demo of Basic Spark Transformations and Actions

# COMMAND ----------

# MAGIC %md
# MAGIC ## Single-RDD Transformations

# COMMAND ----------

# MAGIC %md
# MAGIC #### Filter

# COMMAND ----------

res=sc.parallelize(range(100))
res.filter(lambda x: x%10==1).collect()

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Sample

# COMMAND ----------

# true means with replacement
# random seed is 1, it will use a different seed each time if not specified
res=sc.parallelize(range(100))
res.sample(True,0.1).collect()

# COMMAND ----------

# MAGIC %md
# MAGIC #### flatMap vs Map

# COMMAND ----------

ll=["i am a sheep","i am mcdonald"]

mapres=sc.parallelize(ll).map(lambda x:x.split(" ")).collect()
flatmapres=sc.parallelize(ll).flatMap(lambda x:x.split(" ")).collect()

print "map result:"+str(mapres)
print "flatMap result"+str(flatmapres)



# COMMAND ----------

# MAGIC %md
# MAGIC #### Distinct

# COMMAND ----------

ll=["i am a sheep","i am mcdonald"]

sc.parallelize(ll).flatMap(lambda x:x.split(" ")).distinct().collect()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2-RDD Transformations

# COMMAND ----------

# MAGIC %md
# MAGIC #### Union

# COMMAND ----------

sc.parallelize([1,2,3,4,5,6,7]) \
.union( \
sc.parallelize([5,6,7,8]) \
) \
.collect()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Intersection

# COMMAND ----------

sc.parallelize([1,2,3,4,5,6,7]) \
.intersection( \
sc.parallelize([5,6,7,8]) \
) \
.collect()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Subtract

# COMMAND ----------

sc.parallelize([1,2,3,4,5,6,7]) \
.subtract( \
sc.parallelize([5,6,7,8]) \
) \
.collect()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Cartesian (cross product)

# COMMAND ----------

sc.parallelize([1,2,3,4,5,6,7]) \
.cartesian( \
sc.parallelize([5,6,7,8]) \
) \
.collect()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Actions

# COMMAND ----------

# MAGIC %md
# MAGIC #### count

# COMMAND ----------

sc.parallelize([1,2,3,4,5,6,7,8,2,4,2,1,1,1,1,1]).count()

# COMMAND ----------

# MAGIC %md
# MAGIC #### countByValue

# COMMAND ----------

sc.parallelize([1,2,3,4,5,6,7,8,2,4,2,1,1,1,1,1]).countByValue()

# COMMAND ----------

# MAGIC %md
# MAGIC #### take/takeOrdered/takeSample

# COMMAND ----------

sc.parallelize(["dog", "cat", "ape", "salmon", "gnu"], 2) \
.take(2)

# COMMAND ----------

sc.parallelize(["dog", "cat", "ape", "salmon", "gnu"], 2) \
.takeOrdered(2)

# COMMAND ----------

sc.parallelize(["dog", "cat", "ape", "salmon", "gnu"], 2) \
.takeSample(True, 4)

# COMMAND ----------

# MAGIC %md
# MAGIC #### top

# COMMAND ----------

sc.parallelize([6, 9, 4, 7, 5, 8], 1) \
.top(2)

# COMMAND ----------

# MAGIC %md
# MAGIC #### collect

# COMMAND ----------

sc.parallelize([6, 9, 4, 7, 5, 8], 2) \
.collect() 

# COMMAND ----------

# MAGIC %md
# MAGIC #### reduce

# COMMAND ----------

sc.parallelize(range(1,11), 3) \
.reduce(lambda x,y:x+y)

# COMMAND ----------

# MAGIC %md
# MAGIC #### fold

# COMMAND ----------

sc.parallelize(range(1,11), 2) \
.fold(1,lambda x,y:x+y)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Key-value pair Transformations

# COMMAND ----------

# MAGIC %md
# MAGIC #### keys/values

# COMMAND ----------

a=sc.parallelize(["dog", "tiger", "lion", "cat", "panther", "eagle"], 4) \
.map(lambda x:(len(x), x)) 
print a.collect()
print a.keys().collect()
print a.values().collect()

#Note: keys and values are RDDs

# COMMAND ----------

# MAGIC %md
# MAGIC #### reduceByKey

# COMMAND ----------

#concanate all the words with same length
sc.parallelize(["dog", "tiger", "lion", "cat", "panther", "eagle"], 4) \
.map(lambda x:(len(x), x)) \
.reduceByKey(lambda x,y: x+y) \
.collect()

# COMMAND ----------

# MAGIC %md
# MAGIC #### groupByKey

# COMMAND ----------

sc.parallelize(["dog", "tiger", "lion", "cat", "panther", "eagle"], 4) \
.map(lambda x:(len(x), x)) \
.groupByKey() \
.collect()

# COMMAND ----------

# MAGIC %md
# MAGIC #### sortByKey

# COMMAND ----------

a = sc.parallelize(["dog", "cat", "owl", "gnu", "ant"], 2)
b = sc.parallelize(range(0,a.count()), 2)
c = a.zip(b)
c.sortByKey(True).collect()

# COMMAND ----------

# MAGIC %md
# MAGIC #### mapValues

# COMMAND ----------

sc.parallelize(["dog", "tiger", "lion", "cat", "panther", "eagle"], 4) \
.map(lambda x:(len(x), x)) \
.mapValues(lambda x:"x" + x + "x").collect()

# COMMAND ----------

# MAGIC %md
# MAGIC #### flatMapValues

# COMMAND ----------

sc.parallelize(["dog", "tiger", "lion", "cat", "panther", "eagle"], 4) \
.map(lambda x:(len(x), x)) \
.flatMapValues(lambda x:"x" + x + "x").collect()

# COMMAND ----------

# MAGIC %md
# MAGIC #### join/leftOuterJoin/rightOuterJoin

# COMMAND ----------

v1 = sc.parallelize(["dog", "salmon", "salmon", "rat", "elephant"], 3) \
.keyBy(lambda x:len(x))
print v1.collect()


v2 = sc.parallelize(["dog","cat","gnu","salmon","rabbit","turkey","wolf","bear","bee"], 3) \
.keyBy(lambda x:len(x))
print v2.collect()

print "Join:"+str(v1.join(v2).collect())
print "leftOuterJoin:"+str(v1.leftOuterJoin(v2).collect())
print "rightOuterJoin:"+str(v1.rightOuterJoin(v2).collect())

# COMMAND ----------


