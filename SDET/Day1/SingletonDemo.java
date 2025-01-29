package Day1;

public class SingletonDemo {
    public static void main(String[] args) {
        SingletonObj sObj = SingletonObj.getInstance();
 
        sObj.showMessage();
    }
    
}
