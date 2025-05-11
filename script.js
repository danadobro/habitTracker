// Script File

let h = []; // this is an array of habit objects that we will use to display the habits (unscheduled), and so we can add and delete habits
let sh = []; //array for scheduled habits


// event listener for add new button to show the form
const addNewHabit = document.getElementById("addNew");
const newHabitForm = document.getElementById("habit-form");


addNewHabit.addEventListener('click', (e) => {
    e.preventDefault();
    newHabitForm.classList.toggle("hidden");
});

// event listener for add new button to show the scheduled habit form
const addNewScheduledHabit = document.getElementById("addNewSH");
const newSHHabitForm = document.getElementById("add-scheduled-form");


addNewScheduledHabit.addEventListener('click', (e) => {
    e.preventDefault();
    newSHHabitForm.classList.toggle("hidden");
});


//habit class constructor 
function Habit (name, target) {
    this.name = name;
    this.target = target;
    this.daysCompleted = 0;
    this.logs = []; //to track dates 
    
    // this is a new habit objects that gets created when we add a new habit 

}

const habit_list = document.getElementById("habits"); //reference to the main habits list div

function saveNewHabit(){
    //called on click from add new habit, we should create a habit, and display it in the main div

    //get form input values
    const habit_name = document.getElementById("habit-name").value;
    const target = parseInt(document.getElementById("target").value);
    

    //validate that goal and name exist
    if (target <= 0 || !habit_name){

        alert("Please fill in the habit name and target goal for it!")
        return;
    }

    // create a new habit object with these inputs 
    const newHabit = new Habit(habit_name, target);
    

    // append the habit object to array h 
    h.push(newHabit);


    // append the habit to the habits div which diplays all the habits
    renderHabits();

    //hide the add new habit form again
    newHabitForm.classList.add("hidden");

    // Clear form fields after saving
    document.getElementById("habit-name").value = "";
    document.getElementById("target").value = "";

}


function markUnscheduledHabitCompleted(index) {
    const today = new Date().toISOString().split("T")[0];

    // Prevent double-logging on the same day
    if (h[index].logs.includes(today)) {
        alert("Already marked completed today.");
        return;
    }

    if (h[index].daysCompleted < h[index].target) {
        h[index].daysCompleted++;
        h[index].logs.push(today);
        renderHabits();
    } else {
        alert("Goal already completed."); 
    }




}



//Weekly reaccuring habits with specific days
function ScheduledHabit(name, scheduleDays){
    this.name = name;
    this.scheduleDays = scheduleDays;
    this.completions = [];



}



//creates a new habit and stores it in the list with scheduled habits 
// called on click from add new scheduled habit button taht submits the form and info for the scheduled habit
function saveNewScheduledHabit() {
    const nameInput = document.getElementById("scheduled-name");
    const dayCheckboxes = document.querySelectorAll(".schedule-day:checked");

    const name = nameInput.value.trim();
    const scheduleDays = Array.from(dayCheckboxes).map(cb => cb.value);

    if (!name || scheduleDays.length === 0) {
        alert("Please enter a name and select at least one day.");
        return;
    }

    const newHabit = new ScheduledHabit(name, scheduleDays);
    sh.push(newHabit);

    //reset form
    nameInput.value = "";
    dayCheckboxes.forEach(cb => cb.checked = false);

    renderScheduledHabits();

     //hide the add new habit form again
     newSHHabitForm.classList.add("hidden");


}


//check if the scheduled habit is due today
function isHabitDueToday(habit) {
    const today = new Date();
    const dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const todayName = dayNames[today.getDay()];
    return habit.scheduleDays.includes(todayName);
}


function markScheduledCompleted(index) {
    const today = new Date().toISOString().split("T")[0];

    const alreadyDone = sh[index].completions.some(c => c.date === today);
    if (alreadyDone) return;

    sh[index].completions.push({ date: today, completed: true });
    renderScheduledHabits();
}


function renderScheduledHabits() {
    const container = document.getElementById("scheduled-container");
    container.innerHTML = "";

    // check if due today and if already completed

    sh.forEach((habit, index) => {
        if (isHabitDueToday(habit)) {
            const today = new Date().toISOString().split("T")[0];
            const alreadyCompleted = habit.completions.some(c => c.date === today);

            const div = document.createElement("div");
            div.className = "scheduled-habit";
            div.innerHTML = `
                <h3>${habit.name}</h3>
                <button onclick="markScheduledCompleted(${index})" ${alreadyCompleted ? "disabled" : ""}>
                    ${alreadyCompleted ? "Completed Today" : "Mark as Completed Today"}
                </button>
            `;
            container.appendChild(div);
        }
    });
}




//to render all habits from the array
function renderHabits() {
    const habitContainer = document.getElementById("habit-container");
    habitContainer.innerHTML = "";

    h.forEach((habit, index) => {
        const today = new Date().toISOString().split("T")[0];
        const alreadyDoneToday = habit.logs.includes(today);

        const div = document.createElement("div");
        div.className = "habit";
        div.innerHTML = `
            <h3>${habit.name}</h3>
            <p>${habit.daysCompleted}/${habit.target} completed</p>
            <button onclick="markUnscheduledHabitCompleted(${index})" ${alreadyDoneToday ? "disabled" : ""}>
                ${alreadyDoneToday ? "Completed Today" : "Mark as Completed Today"}
            </button>
        `;

        habitContainer.appendChild(div);
    });
}


// for today and habits due today
const todaySpace = document.getElementById("today-date");
const today = new Date();
todaySpace.textContent = today.toDateString(); //show todays date 









