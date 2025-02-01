package com.fss;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        File f = new File("./name1.txt");
        try {
            f.createNewFile();
            FileWriter fw = new FileWriter(f);
            fw.append("SDET Demo session");
            fw.close();  // Close the FileWriter to ensure data is written

            Scanner sc = new Scanner(f);
            while (sc.hasNextLine()) {
                System.out.println(sc.nextLine());
            }
            sc.close();
        } catch (IOException e) {
            System.out.println("File not found");
        }
    }
}