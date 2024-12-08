package org.iit.kaushik20241270;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class MostScoringQuarterReducer extends Reducer<Text, Text, Text, IntWritable> {
    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        int prevVisitorScore = 0, prevHomeScore = 0, shootSum = 0;

        for (Text value : values) {
            String[] scores = value.toString().split(",");
            int visitorScore = Integer.parseInt(scores[0]);
            int homeScore = Integer.parseInt(scores[1]);

            int visitorScoreDiff = visitorScore - prevVisitorScore;
            int homeScoreDiff = homeScore - prevHomeScore;

            int shoot = Math.abs(visitorScoreDiff - homeScoreDiff);
            shootSum += shoot;

            prevVisitorScore = visitorScore;
            prevHomeScore = homeScore;
        }

        context.write(key, new IntWritable(shootSum));
    }
}

