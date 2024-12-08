package org.iit.kaushik20241270;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class MostScoringQuarterMapper extends Mapper<LongWritable, Text, Text, Text> {

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        String[] fields = line.split(",");

        // Skip the header row based on its length or content
        if (fields[0].equalsIgnoreCase("EVENTID")) {
            return;
        }

        try {
            if (fields[24].isEmpty()) return; // Skip rows where SCORE is empty

            if (fields[3].isEmpty() && fields[26].isEmpty()) return; // Skip rows where HOMEDESCRIPTION, VISITORDESCRIPTION are empty

            String gameId = fields[2].trim();
            String period = fields[5].trim();
            String teamNickname = fields[11].trim();
            String score = fields[24];

            String[] scoreParts = score.split(" - ");
            if (scoreParts.length == 2) {
                String visitorScore = scoreParts[0].trim();
                String homeScore = scoreParts[1].trim();
                context.write(new Text(gameId + "," + period + "," + teamNickname), new Text(visitorScore + "," + homeScore));
            }
        } catch (Exception e) {
            // Handle bad data (e.g., non-numeric score values)
        }
    }
}


