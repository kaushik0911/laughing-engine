package org.iit.kaushik20241270;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class MostScoringQuarterMapper extends Mapper<Object, Text, Text, IntWritable> {
    private final Text teamQuarterKey = new Text();
    private final IntWritable scoreValue = new IntWritable();

    @Override
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        String[] fields = line.split(",");

        // Skip the header row based on its length or content
        if (fields.length < 3 || fields[0].equalsIgnoreCase("TEAM_ID")) {
            return;
        }

        try {
            String teamId = fields[0];
            String quarter = fields[1];
            int score = Integer.parseInt(fields[2]);

            // Key: "TEAM_ID,QUARTER", Value: SCORE
            teamQuarterKey.set(teamId + "," + quarter);
            scoreValue.set(score);
            context.write(teamQuarterKey, scoreValue);
        } catch (NumberFormatException e) {
            // Handle bad data (e.g., non-numeric score values)
        }
    }
}


