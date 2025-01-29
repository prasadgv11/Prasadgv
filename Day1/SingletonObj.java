package Day1;

public class SingletonObj {
    
    private static SingletonObj obj = new SingletonObj();
 
    public static SingletonObj getInstance() {
        return obj;
    }
 
    public void showMessage() {
        System.out.println("Hello Singleton");
    }
}
