package org.iit.kaushik20241270;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class PlayerTotalPointsExtractor {

    public static int extractTotalPoints(String announcerText) {
        // Define the regex to match the player's total points
        String regex = ".*\\((\\d+) PTS\\)";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(announcerText);

        if (matcher.find()) {
            // Group 1 contains the total points in parentheses
            return Integer.parseInt(matcher.group(1));
        }

        // Return 0 if no match is found
        return 0;
    }

    public static void main(String[] args) {
        // Example play texts
        String bowenPlay = "Bowen 25' 3PT Jump Shot (6 PTS) (Carter 1 AST)";
        String carterPlay = "Carter 10' Running Jump Shot (2 PTS)";

        // Extract total points for each player
        int bowenPoints = extractTotalPoints(bowenPlay);
        int carterPoints = extractTotalPoints(carterPlay);

        // Print the results
        System.out.println("Bowen's total points: " + bowenPoints);
        System.out.println("Carter's total points: " + carterPoints);
    }
}
