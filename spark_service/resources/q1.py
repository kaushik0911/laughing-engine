from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col, lag, coalesce, abs, sum as _sum, countDistinct, round
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

# Show the result
df_load.select("GAME_ID", "EVENTID", "PLAYER1_ID", "SHOOT").show()

# Percentage of players who have scored 40 points or more in a single match.

# Step 1: Calculate total points per player per game
player_scores = df_load.groupBy("GAME_ID", "PLAYER1_ID").agg(_sum("SHOOT").alias("TOTAL_POINTS"))

# Step 2: Filter players with 40+ points
players_40_plus = player_scores.filter(col("TOTAL_POINTS") >= 40)

# Step 3: Calculate the total number of unique players per game
total_players_per_game = df_load.select("GAME_ID", "PLAYER1_ID").distinct().groupBy("GAME_ID").agg(countDistinct("PLAYER1_ID").alias("TOTAL_PLAYERS"))

# Step 4: Calculate the number of players who scored 40+ points per game
players_40_plus_per_game = players_40_plus.groupBy("GAME_ID").agg(countDistinct("PLAYER1_ID").alias("PLAYERS_40_PLUS"))

# Step 5: Join the data and calculate percentage
percentage_df = players_40_plus_per_game.join(total_players_per_game, "GAME_ID") \
    .withColumn("PERCENTAGE", round((col("PLAYERS_40_PLUS") / col("TOTAL_PLAYERS")) * 100, 2))

# Show results
percentage_df.select("GAME_ID", "PERCENTAGE").show()

# Stop the Spark session
spark.stop()
