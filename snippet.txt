# laughing-engine

docker exec -it namenode bash

hdfs dfs -mkdir -p /nbadata/

hdfs dfs -put /opt/hadoop/resources/nbadataset.csv /nbadata/

hdfs dfs -put /opt/hadoop/resources/input.csv /nbadata/

hdfs dfs -put /opt/hadoop/resources/nbadatasettest.csv /nbadata/

hdfs dfs -ls /nbadata

yarn jar /opt/hadoop/resources/most_scoring_quarter-1.0-SNAPSHOT.jar org.iit.kaushik20241270.MostScoringQuarterDriver /nbadata/nbadataset.csv /nbadata/output/MostScoringQuarterDriver



yarn jar /opt/hadoop/resources/most_scoring_quarter-1.0-SNAPSHOT.jar org.iit.kaushik20241270.MostScoringQuarterDriver /nbadata/input.csv /nbadata/output/MostScoringQuarterDriver

hdfs dfs -ls /nbadata/output/MostScoringQuarterDriver

hdfs dfs -cat /nbadata/output/MostScoringQuarterDriver


yarn jar /opt/hadoop/resources/most_scored_player-1.0-SNAPSHOT.jar org.iit.kaushik20241270.TopPlayerJob /nbadata/nbadataset.csv /nbadata/output/TopPlayerJob

hdfs dfs -cat /nbadata/output/TopPlayerJob/part-r-00000

hdfs dfs -ls /nbadata/output/TopPlayerJob

hdfs dfs -rm -R /nbadata/output/TopPlayerJob

hdfs dfs -cat /nbadata/output/MostScoringQuarterDriver/part-r-00000


hdfs dfs -rm -R /nbadata/output

yarn jar /opt/hadoop/resources/most_scored_player-1.0-SNAPSHOT.jar org.iit.kaushik20241270.TopPlayerJob /nbadata/nbadataset.csv /nbadata/output/TopPlayerJob


Allen Iverson   1249



CREATE EXTERNAL TABLE dataset (id INT,name STRING,age INT,salary FLOAT) STORED AS TEXTFILE LOCATION '/user/hive/data/data.csv' TBLPROPERTIES ('skip.header.line.count'='1');


CREATE TABLE dataset (id INT,name STRING,age INT,salary FLOAT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION 'hdfs://hive-namenode:8020/user/hive/database' TBLPROPERTIES ('skip.header.line.count'='1');

LOAD DATA INPATH 'hdfs://hive-namenode:8020/user/hive/data/data.csv' INTO TABLE dataset;


CREATE EXTERNAL TABLE dataset (id INT, name STRING, age INT, salary FLOAT) STORED AS TEXTFILE LOCATION 'hdfs://hive-namenode:8020/user/hive/database' TBLPROPERTIES ('skip.header.line.count'='1');

LOAD DATA INPATH 'hdfs://hive-namenode:8020/user/hive/data/data.csv' INTO TABLE dataset;

CREATE TABLE recharge (id INT, name STRING, age INT, salary FLOAT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION 'hdfs://hive-namenode:8020/user/hive/warehouse/telecom.db/recharge';


INSERT INTO recharge (id, name, age, salary) VALUES (100, "fernando", 18, 30);


CREATE TABLE recharge ( cell_no INT, city STRING, name STRING, price FLOAT ) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION 'hdfs://hive-namenode:8020/user/hive/warehouse/telecom.db/recharge';

INSERT INTO recharge (cell_no,city,name,price) VALUES (999090,"sl","fernando",30.0);

LOAD DATA LOCAL INPATH '/opt/hadoop/resources/recharge.input' INTO TABLE recharge;

hdfs dfs -put -f /opt/hadoop/resources/nbadataset.csv hdfs://hive-namenode:8020/user/hive/warehouse/nba.db/


LOAD DATA INPATH '/user/hive/data/data.csv' INTO TABLE dataset;

LOAD DATA INPATH 'hdfs://hive-namenode:8020/user/hive/warehouse/nba.db/nbadataset.csv' INTO TABLE dataset;




<!--  ------------- -->

spark/bin/spark-shell --master spark://spark-master:7077 --conf "spark.eventLog.enabled=true" --conf "spark.eventLog.dir=/tmp/spark-events"


val df = spark.read.csv("hdfs://spark-namenode:9000/nbadata/nbadataset.csv")


park/bin/spark-submit --master local /opt/hadoop/resources/example.py