package Day1;

import java.util.HashSet;

public class Hashset {

     public static void main(String[] args) {
    
        HashSet<String> names = new HashSet<>();
        names.add("Prasad");
        names.add("Rahul");
        names.add("Arun");
        names.add("Arjun");
        names.add("Arjun");  
    

        System.out.println("HashSet of unique names: " + names);
    }
    
}
