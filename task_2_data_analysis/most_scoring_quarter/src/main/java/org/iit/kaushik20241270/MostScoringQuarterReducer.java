package org.iit.kaushik20241270;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class MostScoringQuarterReducer extends Reducer<Text, IntWritable, Text, Text> {
    private Map<String, Integer> teamQuarterScores = new HashMap<>();
    private Text outputKey = new Text();
    private Text outputValue = new Text();

    @Override
    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
        String[] teamQuarter = key.toString().split(",");
        String teamId = teamQuarter[0];
        String quarter = teamQuarter[1];

        // Sum the scores for this team and quarter
        int totalScore = 0;
        for (IntWritable value : values) {
            totalScore += value.get();
        }

        // Update the teamQuarterScores map
        String teamKey = teamId;
        teamQuarterScores.merge(teamKey + "," + quarter, totalScore, Integer::sum);
    }

    @Override
    protected void cleanup(Context context) throws IOException, InterruptedException {
        // Identify the most scoring quarter for each team
        Map<String, String> highestScoringQuarters = new HashMap<>();
        Map<String, Integer> highestScores = new HashMap<>();

        for (Map.Entry<String, Integer> entry : teamQuarterScores.entrySet()) {
            String[] teamQuarter = entry.getKey().split(",");
            String teamId = teamQuarter[0];
            String quarter = teamQuarter[1];
            int score = entry.getValue();

            // Compare and update highest scores for the team
            if (!highestScores.containsKey(teamId) || score > highestScores.get(teamId)) {
                highestScores.put(teamId, score);
                highestScoringQuarters.put(teamId, quarter);
            }
        }

        // Write results to the context
        for (String teamId : highestScores.keySet()) {
            outputKey.set(teamId);
            outputValue.set("Quarter: " + highestScoringQuarters.get(teamId) + ", Score: " + highestScores.get(teamId));
            context.write(outputKey, outputValue);
        }
    }
}

