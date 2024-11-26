# laughing-engine

docker exec -it namenode bash

hdfs dfs -mkdir -p /nbadata/

hdfs dfs -put /opt/hadoop/resources/nbadataset.csv /nbadata/

hdfs dfs -put /opt/hadoop/resources/input.csv /nbadata/

hdfs dfs -ls /nbadata

yarn jar /opt/hadoop/resources/most_scoring_quarter-1.0-SNAPSHOT.jar org.iit.kaushik20241270.MostScoringQuarterDriver /nbadata/nbadataset.csv /nbadata/output/MostScoringQuarterDriver



yarn jar /opt/hadoop/resources/most_scoring_quarter-1.0-SNAPSHOT.jar org.iit.kaushik20241270.MostScoringQuarterDriver /nbadata/input.csv /nbadata/output/MostScoringQuarterDriver

hdfs dfs -ls /nbadata/output/MostScoringQuarterDriver

hdfs dfs -cat /nbadata/output/MostScoringQuarterDriver