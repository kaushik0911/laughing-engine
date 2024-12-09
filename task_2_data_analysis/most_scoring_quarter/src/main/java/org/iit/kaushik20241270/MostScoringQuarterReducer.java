package org.iit.kaushik20241270;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class MostScoringQuarterReducer extends Reducer<Text, Text, Text, Text> {
    // Map to store the highest score and corresponding period for each team
    private Map<String, Integer> teamMaxScoreMap = new HashMap<>();
    private Map<String, String> teamMaxQuarterMap = new HashMap<>();

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

        // Extract team nickname and period from the key
        String[] keyParts = key.toString().split(",");
        String gameId = keyParts[0];
        String period = keyParts[1];
        String teamNickname = keyParts[2];

        // Construct a unique team identifier
        String teamKey = teamNickname;

        // Check if the current period's shootSum is the maximum for this team
        if (!teamMaxScoreMap.containsKey(teamKey) || shootSum > teamMaxScoreMap.get(teamKey)) {
            teamMaxScoreMap.put(teamKey, shootSum);
            teamMaxQuarterMap.put(teamKey, "Game: " + gameId + ", Period: " + period);
        }
    }

    @Override
    protected void cleanup(Context context) throws IOException, InterruptedException {
        // Write the most scoring quarter for each team
        for (Map.Entry<String, Integer> entry : teamMaxScoreMap.entrySet()) {
            String teamNickname = entry.getKey();
            int maxScore = entry.getValue();
            String maxQuarter = teamMaxQuarterMap.get(teamNickname);

            context.write(new Text("Team: " + teamNickname ), new Text(maxQuarter));
        }
    }
}
