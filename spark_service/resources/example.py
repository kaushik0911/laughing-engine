from pyspark.sql import SparkSession

# Initialize the SparkSession
spark = SparkSession.builder \
    .appName("ExampleSparkJob") \
    .getOrCreate()

# Read a CSV file from HDFS.
df_load = spark.read.csv(
    'hdfs://spark-namenode:9000/nbadata/nbadataset.csv',
    sep=',',
    inferSchema=True,
    header=True)


df_load.show(5)

# Stop the Spark session
spark.stop()
