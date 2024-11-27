package org.iit.kaushik20241270;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class PlayerScoreMapper extends Mapper<Object, Text, Text, IntWritable> {
    private final Text playerName = new Text();
    private final IntWritable score = new IntWritable();

    @Override
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
        // Split CSV record by commas
        String line = value.toString();
        String[] fields = line.split(",");

        // Skip the header row based on its length or content
        if (fields[0].equalsIgnoreCase("GAME_ID")) {
            return;
        }

        try {
            // Ensure we have enough fields and extract relevant columns
            if (fields.length >= 3) { // Adjust if needed
                String gameId = fields[0];
                String homeCommentary = fields[1];
                // String visitorCommentary = fields[26];
                String player1Name = fields[2];

                String commentary;

                if (!homeCommentary.isEmpty() && !player1Name.isEmpty()) {
                    commentary = homeCommentary;
                } else {
                   return;
                }

                int totalScore = PlayerTotalPointsExtractor.extractTotalPoints(commentary);

                // Emit the game id, player's name and score
                playerName.set(gameId + "," + player1Name);
                score.set(totalScore);
                context.write(playerName, score);

            }
        } catch (Exception e) {
            // Handle malformed records (optional)
            e.printStackTrace();
        }
    }
}
