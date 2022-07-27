/**
 * Updates the current color, distance and motor status calling teh corresponding methods
 */
function updateStatus() {
  // Update current color based on Open CV
  (async () => await updateCurrentShapeOpenCV())();

  // Update motor status based on the position
  (async () => await updateMotorStatus())();

  (async () => await updateCurrentShapeDistance())();

  (async () => await updateDistance())();
}

/**
 * Update the current color based on OpenCV
 */
 async function updateCurrentShapeOpenCV() {
  try {
        // Request shape from server
        const requestResult = await requestShapeFromOpenCV()
        // Get the HTML element where the status is displayed
        const triangle_open_cv = document.getElementById('triangle_open_cv')
        triangle_open_cv.innerHTML = requestResult.data[0]
        const square_open_cv = document.getElementById('square_open_cv')
        square_open_cv.innerHTML = requestResult.data[1]
        const circle_open_cv = document.getElementById('circle_open_cv')
        circle_open_cv.innerHTML = requestResult.data[2]

    } catch (e) {
        console.log('Error getting the shape based on OpenCV', e)
        updateStatus('Error getting the shape based on OpenCV')
    }
}

/**
 * Function to request the server to update the current color based on OpenCV
 */
 function requestShapeFromOpenCV () {
  try {
    // Make request to server
    return axios.get('/get_shape_from_opencv')
  } catch (e) {
    console.log('Error getting the status', e)
  }
}

/**
 * Function to request the server to start the motor
 */
 function requestStartMotor () {
  try {
    return axios.get('/start_motor')
  } catch (e) {
    console.log('Error is : ', e)
  }
}

/**
 * Function to request the server to stop the motor
 */
function requestStopMotor () {
  try {
    return axios.get('/stop_motor')
  } catch (e) {
    console.log('Enter error message', e)
  }
}

/**
 * Update the status of the motor
 * @param {String} status
 */
 function updateMotorStatus() {
  // Get the HTML element where the status is displayed
  axios.get('/motor_status')
  .then((response) => {
    const motor_status_html_element = document.getElementById('motorStatus')
    if(response.data.success){
      motor_status_html_element.innerHTML = "Motor is running and rotating at " + response.data.position
    }
    else{
      motor_status_html_element.innerHTML = "Motor is Stopped"
    }
  });
}

/**

 * Update the current color based on distance sensor
 */
async function updateDistance() {
  try {
    const distance_element = document.getElementById("distance")
    distance_element.innerHTML = " Calculating Please Wait... (May take upto 1 Minute)"

    console.log("Accessing")
    const distanceData = await requestDistance()
    console.log(distanceData)

    distance_element.innerHTML = " " + distanceData.data
    //updateCurrentColorDistance()
  } catch (e) {
    console.log('Wrong distance', e)
  }
}

/**
 * Function to request the server to get the distance from
 * the rod to the ultrasonic sensor
 */
 async function requestDistance () {
  //...
  try {
    return axios.get('/get_distance')
  } catch (e) {
    console.log('Error getting the distance', e)
  }
}

/**
 * Update the current color based on distance sensor
 */
async function updateCurrentShapeDistance() {
  try {
    // Request color from server
    const requestResult = await requestShapeFromDistance()
    // Get the HTML element where the status is displayed
    const green_distance = document.getElementById('triangle_from_distance')
    green_distance.innerHTML = requestResult.data[0]
    const purple_distance = document.getElementById('square_from_distance')
    purple_distance.innerHTML = requestResult.data[1]
    const yellow_distance = document.getElementById('circle_from_distance')
    yellow_distance.innerHTML = requestResult.data[2]
  } catch (e) {
    console.log('Error getting the color based on distance', e)
    // updateStatus('Error getting the color based on distance')
  }
}

/**
 * Function to request the server to get the color based
 * on distance only
 */
function requestShapeFromDistance () {
  try {
    return axios.get('/get_shape_from_distance')
  } catch (e) {
    console.log('Error getting the status', e)
    // updateStatus('Error getting the status')
  }
}
