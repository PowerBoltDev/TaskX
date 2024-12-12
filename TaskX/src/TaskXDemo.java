import java.time.Duration;
import java.time.LocalDateTime;




public class TaskXDemo {
    public static void main(String[] args) {
        TaskManager manager = new TaskManager();

        Task projectTask = manager.addTask( 
        "Complete Project proposal",
        "Finish the first draft of the project proposal",
        Priority.HIGH,
        LocalDateTime.now().plusDays(3)
        );
    

    //Simulate working on a task
    projectTask.startTimer();
    //Simulate working on a task
    try {
        Thread.sleep(5000); // this is 5 seconds of work
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    Duration timeSpent = projectTask.stopTimer();

    //Get Summary
    manager.generateDailySummary();
}


}
