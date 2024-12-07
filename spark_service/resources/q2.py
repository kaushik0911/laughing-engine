from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col, lag, coalesce, abs, sum as _sum, countDistinct, round, max, when, lit, first, last, desc, row_number
from pyspark.sql.window import Window

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

df_load = df_load\
            .na\
            .drop(subset=["SCORE"])

df_load = df_load\
                .withColumn("VISITOR_SCORE", split(col("SCORE"), " - ")\
                    .getItem(0).cast("int"))\
                .withColumn("HOME_SCORE", split(col("SCORE"), " - ")\
                    .getItem(1).cast("int"))

df_load.select("EVENTID", "SCORE", "VISITOR_SCORE", "HOME_SCORE").show()

# Define a window partitioned by GAME_ID and ordered by EVENTID
window_spec = Window.partitionBy("GAME_ID").orderBy("EVENTID")

# Add columns for the previous row's VISITOR_SCORE and HOME_SCORE within each game
df_load = df_load\
                .withColumn("PREV_VISITOR_SCORE", coalesce(lag("VISITOR_SCORE").over(window_spec), col("VISITOR_SCORE") * 0)) \
                .withColumn("PREV_HOME_SCORE", coalesce(lag("HOME_SCORE").over(window_spec), col("HOME_SCORE") * 0))

# Calculate the differences
df_load = df_load\
                .withColumn("VISITOR_SCORE_DIFF", (col("VISITOR_SCORE") - col("PREV_VISITOR_SCORE")).cast("int")) \
                .withColumn("HOME_SCORE_DIFF", (col("HOME_SCORE") - col("PREV_HOME_SCORE")).cast("int"))

df_load = df_load\
                .withColumn("SHOOT", abs(col("VISITOR_SCORE_DIFF") - col("HOME_SCORE_DIFF")))


# The total number of matches lost by each team.

# Filter rows where at least one of the columns is not NULL
filtered_df = df_load.filter(~((df_load.HOMEDESCRIPTION.isNull()) & (df_load.VISITORDESCRIPTION.isNull())))

home_team = filtered_df.filter(col("HOMEDESCRIPTION").isNotNull()) \
    .groupby("GAME_ID") \
    .agg(first("PLAYER1_TEAM_ABBREVIATION").alias("HOME_TEAM"))

visitor_team = filtered_df.filter(col("VISITORDESCRIPTION").isNotNull()) \
    .groupby("GAME_ID") \
    .agg(first("PLAYER1_TEAM_ABBREVIATION").alias("VISITOR_TEAM"))

result_df = filtered_df.join(home_team, on="GAME_ID", how="left") \
                        .join(visitor_team, on="GAME_ID", how="left")

# Get the last event for each game
window_spec = Window.partitionBy("GAME_ID").orderBy(desc("EVENTID"))
last_event_df = result_df.withColumn("rank", row_number().over(window_spec)) \
    .filter(col("rank") == 1) \
    .drop("rank")

# Determine the losing team
losing_team_df = last_event_df.withColumn(
    "LOSING_TEAM", when(col("VISITOR_SCORE") < col("HOME_SCORE"), col("VISITOR_TEAM")).otherwise(col("HOME_TEAM"))
)

# Count the total losses for each team
loss_count_df = losing_team_df.groupBy("LOSING_TEAM").count() \
    .withColumnRenamed("count", "TOTAL_LOSSES") \
    .orderBy(desc("TOTAL_LOSSES"))

# Show the result
loss_count_df.show()
