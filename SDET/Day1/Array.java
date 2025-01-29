package Day1;

public class Array {
public static void main(String[] args) {

    //array of integers with 10 elements
    int[] array = {12, 2, 3, 4, 6, 8, 10, 1, 18, 22};

    //largest and smallest element in the array
    int largest = array[0];
    int smallest = array[0];
    int sum = 0;

    for (int i = 0; i < array.length; i++) {
        if (array[i] > largest) {
            largest = array[i];
        }
        if (array[i] < smallest) {
            smallest = array[i];
        }
        sum += array[i];
    }
// Reverse the array
int[] reversedArray = new int[array.length];
for (int i = 0; i < array.length; i++) {
    reversedArray[i] = array[array.length - 1 - i];
}

// The average of all elements in the array
double average = (double) sum / array.length;

// Print the results
System.out.println("Original array: ");
for (int num : array) {
    System.out.print(num + " ");
}
System.out.println();

System.out.println("Largest element: " + largest);
System.out.println("Smallest element: " + smallest);

System.out.println("Reversed array: ");
for (int num : reversedArray) {
    System.out.print(num + " ");
}
System.out.println();

System.out.println("Sum of all elements: " + sum);
System.out.println("Average of all elements: " + average);
}
}
