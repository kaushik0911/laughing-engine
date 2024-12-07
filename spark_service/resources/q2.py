from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col, lag, coalesce, abs, sum as _sum, countDistinct, round, max, when, lit, first, last, desc
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

# Calculate total score per game for home and visitor teams
game_scores = (
    filtered_df.groupBy("GAME_ID")
    .agg(
        max("HOME_SCORE").alias("HOME_TOTAL_SCORE"),
        max("VISITOR_SCORE").alias("VISITOR_TOTAL_SCORE"),
        first("PLAYER1_TEAM_ABBREVIATION").alias("HOME_TEAM"),
        last("PLAYER1_TEAM_ABBREVIATION").alias("VISITOR_TEAM"),
    )
)

game_scores.show()


# Determine the winning and losing teams dynamically for each game
game_results = game_scores.withColumn(
    "WINNING_TEAM",
    when(col("HOME_TOTAL_SCORE") > col("VISITOR_TOTAL_SCORE"), col("HOME_TEAM"))
    .when(col("HOME_TOTAL_SCORE") < col("VISITOR_TOTAL_SCORE"), col("VISITOR_TEAM"))
    .otherwise(lit(None)),
).withColumn(
    "LOSING_TEAM",
    when(col("HOME_TOTAL_SCORE") < col("VISITOR_TOTAL_SCORE"), col("HOME_TEAM"))
    .when(col("HOME_TOTAL_SCORE") > col("VISITOR_TOTAL_SCORE"), col("VISITOR_TEAM"))
    .otherwise(lit(None)),
)

# -----------------
"""

# Count losses for each team across all games
team_loss_counts = (
    game_results.groupBy("LOSING_TEAM")
    .count()
    .withColumnRenamed("count", "TOTAL_LOSSES")
    .orderBy(desc("TOTAL_LOSSES"))
)

print("Total matches lost by each team:")
team_loss_counts.show()
"""