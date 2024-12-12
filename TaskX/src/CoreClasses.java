import java.time.LocalDateTime;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.UUID;
import java.util.List;
import java.util.ArrayList;
import java.util.stream.Collectors;

enum Priority {
    HIGH,
    MEDIUM,
    LOW
}

//This class is used to create the foundation of the individual tasks
class Task {
    private final String id;
    private String title;
    private String description;
    private Priority priority;
    private LocalDateTime dueDate;
    private LocalDateTime createdAt;

    //The code below this is used to Track time
    private Duration totalTrackedTime;
    private LocalDateTime currentTimerStart;
    private boolean isTimerRunning;

    public Task(String title, String description, Priority priority, LocalDateTime dueDate) {

        this.id = UUID.randomUUID().toString();
        this.title = title;
        this.description = description;
        this.priority = priority;
        this.dueDate = dueDate;
        this.createdAt = LocalDateTime.now();
        this.totalTrackedTime = Duration.ZERO;
        this.isTimerRunning = false;
    }

    //this class is used to start the timer
public void startTimer() {
    if (!isTimerRunning) {
        currentTimerStart = LocalDateTime.now();
        isTimerRunning = true;
    }
}

//Stop function for the timer
public Duration stopTimer() {
    if (isTimerRunning) {
        LocalDateTime now = LocalDateTime.now();
        Duration sessionTime = Duration.between(currentTimerStart, now);
        totalTrackedTime = totalTrackedTime.plus(sessionTime);
        isTimerRunning = false;
        return sessionTime;
    }
    return Duration.ZERO;
   }

   //Manually add time
   public void addManualTime(Duration duration) {
    totalTrackedTime = totalTrackedTime.plus(duration);
   }

   //Getters and Setters
   public String getId() {return id;}
   public String getTitle() {return title;}
   public void setTitle(String title) {this.title = title;}
   public Priority getPriority() {return priority;}
   public void setPriority(Priority priority) {this.priority = priority;}
   public Duration getTotalTrackedTime() {return totalTrackedTime;}
   public LocalDateTime getDueDate() {return dueDate;}
}


//This class is to make the main Task Manager Functionality
class TaskManager {
    private List<Task> tasks;

    public TaskManager() {
        this.tasks = new ArrayList<>();
    }

    //Add Task Function
    public Task addTask(String title, String description, Priority priority, LocalDateTime dueDate) {
        Task newTask = new Task(title, description, priority, dueDate);
        tasks.add(newTask);
        return newTask;
    }

    //Remove a task via ID
    public boolean removeTask(String taskId) {
        return tasks.removeIf(task -> task.getId().equals(taskId));
    }

    //Get tasks by priority
    public List<Task> getTasksByPriority(Priority priority) {
        return tasks.stream()
                .filter(task -> task.getPriority() == priority)
                .collect(Collectors.toList());
    }

    //Get tasks due today or overdue
    public List<Task> getTasksDueTodayOrOverdue() {
        LocalDateTime now = LocalDateTime.now();
        return tasks.stream()
                .filter(task -> task.getDueDate().equals(now) || task.getDueDate().isBefore(now))
                .collect(Collectors.toList());
    }

    //Generate Daily Summary
    public void generateDailySummary() {
        System.out.println("Daily Summary: ");
        tasks.stream()
                .filter(task -> task.getTotalTrackedTime().getSeconds() > 0)
                .forEach(task -> {
                    System.out.printf("Task: %s, Time Spent %d minutes%n",
                            task.getTitle(),
                            task.getTotalTrackedTime().getSeconds() / 60
                            );
                });
    }
}






