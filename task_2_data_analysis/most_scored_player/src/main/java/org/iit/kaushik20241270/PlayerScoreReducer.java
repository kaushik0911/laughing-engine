package org.iit.kaushik20241270;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.HashMap;

public class PlayerScoreReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    private final HashMap<String, Integer> playerScores = new HashMap<>(); // To store total scores per player

    @Override
    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
        int maxScore = 0;

        // Calculate the maximum score for this (gameId, player_name) key
        for (IntWritable value : values) {
            maxScore = Math.max(maxScore, value.get());
        }

        // Extract the player's name from the key
        String[] keyParts = key.toString().split(",", 2); // Split "gameId,player_name"
        String playerName = keyParts[1];

        // Add the max score for this player to the total
        playerScores.put(playerName, playerScores.getOrDefault(playerName, 0) + maxScore);
    }

    @Override
    protected void cleanup(Context context) throws IOException, InterruptedException {
        // Find the player with the highest total score
        String topPlayer = null;
        int highestScore = 0;

        for (HashMap.Entry<String, Integer> entry : playerScores.entrySet()) {
            if (entry.getValue() > highestScore) {
                highestScore = entry.getValue();
                topPlayer = entry.getKey();
            }
        }

        // Write the top player and their total score
        context.write(new Text(topPlayer), new IntWritable(highestScore));
    }
}

