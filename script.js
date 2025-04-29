// Script File
const addNewHabit = document.getElementById("addNew");
const newHabitForm = document.getElementById("habit-form");


addNewHabit.addEventListener('click', (e) => {
    e.preventDefault();
    newHabitForm.classList.toggle("hidden");
});

//habit class constructor 
function Habit (name, notes, goal, days_completed) {
    this.name = name;
    this.notes = notes;
    this.goal = goal;
    this.days_completed = days_completed;
    // this is a new habit objects that gets created when we add a new habit 

}

let h = []; // this is an array of habit objects that we will use to display the habits, and so we can add and delete habits

const habit_list = document.getElementById("habits"); //reference to the main habits list div

function saveNewHabit(){
    //called on click from add new habit, we should create a habit, and display it in the main div

    //get form input values
    const habit_name = document.getElementById("habit-name").value;
    const goal_number = parseInt(document.getElementById("habit-goal").value);
    const notes = document.getElementById("habit-notes").value;

    //validate that goal and name exist
    if (goal_number <= 0 || !habit_name){

        alert("Please fill in the habit name and goal!")
        return;
    }

    // create a new habit object with these inputs 
    const newHabit = new Habit(habit_name, notes, goal_number, 0);
    

    // append the habit object to array h 
    h.push(newHabit);


    // append the habit to the habits div which diplays all the habits
    renderHabits();

    //hide the add new habit form again
    newHabitForm.classList.add("hidden");

    // Clear form fields after saving
    document.getElementById("habit-name").value = "";
    document.getElementById("habit-goal").value = "";
    document.getElementById("habit-notes").value = "";

}

//to render all habits from the array
function renderHabits(){
    //clear current list
    habit_list.innerHTML="";

    h.forEach((habit, index) => {
        const habitDiv = document.createElement("div");
        habitDiv.classList.add("habit-item");

        const progress = (habit.days_completed / habit.goal) * 100;

        habitDiv.innerHTML = `
            <h3>${habit.name}</h3>
            <p><strong>Goal:</strong> ${habit.goal} days</p>
            <p><strong>Notes:</strong> ${habit.notes}</p>
            <p><strong>Completed:</strong> ${habit.days_completed} days</p>
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: ${progress}%;"></div>
            </div>
        `;

        habit_list.appendChild(habitDiv);
    });
}







