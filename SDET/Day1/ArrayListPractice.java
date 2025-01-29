package Day1;

import java.util.ArrayList;
import java.util.Collections;
;

public class ArrayListPractice {
    public static void main(String[] args) {
        // Create an ArrayList of integers, add some elements, and print the list
     
     ArrayList <Integer> arrays=new ArrayList<>();

     System.out.println("ArrayList Example:");
     
     arrays.add(10);
     arrays.add(5);
     arrays.add(20);
     arrays.add(15);

        // Sort the list in ascending order and print the sorted list
        Collections.sort(arrays);
        System.out.println("Sorted ArrayList: " + arrays);



}
    
}

