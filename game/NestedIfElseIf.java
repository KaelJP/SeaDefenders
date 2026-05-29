import javax.swing.JOptionPane;

public class NestedIfElseIf {
    public static void main(String[] args) {

        int number1,number2,number3;
        int largest=0;

        number1 = Integer.parseInt(JOptionPane.showInputDialog("Enter number1: "));
        number2 = Integer.parseInt(JOptionPane.showInputDialog("Enter number2: "));
        number3 = Integer.parseInt(JOptionPane.showInputDialog("Enter number3: "));

        if(number1 > number2)
                largest = number1;
        else
            largest = number2;

        if(number3 > largest)
            largest = number3;

        System.out.print("For nos. " + number1 + " " + number2 + " " + number3 + " "
        + "The Largest is " + largest);
    }
}