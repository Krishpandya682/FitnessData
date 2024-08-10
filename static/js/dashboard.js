window.onload = async function() {
    try {
        // Fetch the calories data
        const caloriesRes = await fetch('/calories/data');
        const caloriesData = await caloriesRes.json();
        
        // Initialize a variable to hold the total calories burned
        let totalCaloriesBurned = 0;

        // Loop through the points array and sum up the calories
        caloriesData.point.forEach(point => {
            if (point.value && point.value.length > 0) {
                totalCaloriesBurned += point.value[0].fpVal;  // Add the fpVal (calories) to the total
            }
        });

        // Display the total calories burned on the dashboard
        document.getElementById('calories-burned').textContent = `Active Calories Burned: ${totalCaloriesBurned}`;
        
        // Fetch and display the steps and active minutes in a similar manner
        const stepsRes = await fetch('/steps/data');
        const stepsData = await stepsRes.json();
        let totalSteps = 0;

        stepsData.point.forEach(point => {
            if (point.value && point.value.length > 0) {
                totalSteps += point.value[0].intVal;  // Assuming steps are stored in intVal
            }
        });

        document.getElementById('steps-taken').textContent = `Number of Steps: ${totalSteps}`;

        const activeMinutesRes = await fetch('/active-minutes/data');
        const activeMinutesData = await activeMinutesRes.json();
        let totalActiveMinutes = 0;

        activeMinutesData.point.forEach(point => {
            if (point.value && point.value.length > 0) {
                totalActiveMinutes += point.value[0].intVal;  // Assuming active minutes are stored in intVal
            }
        });

        document.getElementById('active-minutes').textContent = `Total Active Minutes: ${totalActiveMinutes}`;
        
    } catch (error) {
        console.error('Error fetching fitness data:', error);
    }
};
