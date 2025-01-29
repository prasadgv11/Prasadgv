package Day1;

import java.util.HashMap;


public class hashmap {

    public static void main(String[] args) {
        // Create a HashMap to store student names as keys and their scores as values
        HashMap<String, Integer> studentScores = new HashMap<>();
        studentScores.put("Prasd", 97);
        studentScores.put("Rahul", 98);
        studentScores.put("Arjun", 99);

        System.out.println("HashMap of student scores: " + studentScores);
    }
    
}
