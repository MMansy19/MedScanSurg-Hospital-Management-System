function updateDoctors() {
  // Get the selected surgery type
  // var surgeryType = document.getElementById("SurgeryType").value;

  // // Get the imageRowContainer
  // var imageRowContainer = document.getElementById("imageRowContainer");

  // // Clear existing content in imageRowContainer
  // imageRowContainer.innerHTML = "";

  // // Define a map of surgery types to corresponding surgeon data
  // var surgeonData = {
  //   "Orthopedic Surgery": [
  //     {
  //       name: "Dr. Shaun Murphy",
  //       specialization: "Orthopedic Specialist",
  //       image: "doctor1.jpg",
  //     },
  //     {
  //       name: "Dr. Amr Safwat",
  //       specialization: "Orthopedic Specialist",
  //       image: "doctor2.jpg",
  //     },
  //     {
  //       name: "Dr. Reznik",
  //       specialization: "Orthopedic Specialist",
  //       image: "doctor3.jpg",
  //     },
  //   ],
  //   "Cardiovascular Surgery": [
  //     {
  //       name: "Dr. Brown",
  //       specialization: "Cardiovascular Specialist",
  //       image: "doctor4.jpg",
  //     },
  //     {
  //       name: "Dr. Davis",
  //       specialization: "Cardiovascular Specialist",
  //       image: "doctor5.jpg",
  //     },
  //     {
  //       name: "Dr. Miller",
  //       specialization: "Cardiovascular Specialist",
  //       image: "doctor6.jpg",
  //     },
  //   ],
  //   Neurosurgery: [
  //     {
  //       name: "Dr. Steve",
  //       specialization: "Neurosurgery Specialist",
  //       image: "doctor7.jpg",
  //     },
  //     {
  //       name: "Dr. Menz",
  //       specialization: "Neurosurgery Specialist",
  //       image: "doctor8.jpeg",
  //     },
  //     {
  //       name: "Dr. Imam",
  //       specialization: "Neurosurgery Specialist",
  //       image: "doctor9.jpg",
  //     },
  //   ],
  // };

  // // Check if the selected surgery type has corresponding data
  // if (surgeonData.hasOwnProperty(surgeryType)) {
  //   // Add images, names, and specializations to imageRowContainer
  //   surgeonData[surgeryType].forEach(function (doctor) {
  //     // Create container for each doctor
  //     var doctorContainer = document.createElement("div");
  //     doctorContainer.classList.add("doctor-container");

  //     // Create image element
  //     var imgElement = document.createElement("img");
  //     imgElement.src = "./image/" + doctor.image;
  //     imgElement.alt = "Surgeon Image";
  //     doctorContainer.appendChild(imgElement);

  //     // Create text element for the doctor's name
  //     var nameElement = document.createElement("p");
  //     nameElement.textContent = doctor.name;
  //     doctorContainer.appendChild(nameElement);

  //     // Create text element for the doctor's specialization
  //     var specializationElement = document.createElement("p");
  //     specializationElement.textContent = doctor.specialization;
  //     doctorContainer.appendChild(specializationElement);

  //     // Append the container to imageRowContainer
  //     imageRowContainer.appendChild(doctorContainer);
  //   });

  //   // Populate the DoctorName select element
  //   var doctorNameSelect = document.getElementById("DoctorName");
  //   doctorNameSelect.innerHTML = "";
  //   surgeonData[surgeryType].forEach(function (doctor) {
  //     var optionElement = document.createElement("option");
  //     optionElement.value = doctor.name;
  //     optionElement.textContent = doctor.name;
  //     doctorNameSelect.appendChild(optionElement);
  //   });
  // }

  // Show the imageRowContainer and DoctorName select element
  document.getElementById("testDoctorDiv").style.display = "block";
  document.getElementById("DoctorSelect").style.display = "block";
}

function updateTestTypes() {
  var scanType = document.getElementById("scanType").value;
  var testTypeDiv = document.getElementById("testTypeDiv");
  var testTypeSelect = document.getElementById("testType");

  // Clear existing options
  testTypeSelect.innerHTML = "";

  switch (scanType) {
    case "MRI":
      testTypeDiv.style.display = "block";
      addOption(testTypeSelect, "Type", "null");
      addOption(testTypeSelect, "Cardiac MRI", "Cardiac MRI");
      addOption(testTypeSelect, "Functional MRI", "Functional MRI");
      addOption(testTypeSelect, "MRA", "MRA");
      addOption(testTypeSelect, "MRV", "MRV");

      break;
    case "CT Scan":
      testTypeDiv.style.display = "block";
      addOption(testTypeSelect, "Type", "null");
      addOption(testTypeSelect, "CT Scan Bones ", "CT Scan Bones");
      addOption(testTypeSelect, "CT Scan Brain", "CT Scan Brain ");
      addOption(
        testTypeSelect,
        "CT Scan Arthrography",
        "CT Scan Arhtrography "
      );
      addOption(testTypeSelect, "CT Scan Chest", "CT Scan Chest ");

      break;
    case "PET Scan":
      testTypeDiv.style.display = "block";
      addOption(testTypeSelect, "Type", "null");
      addOption(testTypeSelect, "CardiacScan PET ", "Cardiac PET Scan");
      addOption(testTypeSelect, "Full PET Scan", "Full PET Scan");
      break;
    case "UltraSound Scan":
      testTypeDiv.style.display = "block";
      addOption(testTypeSelect, "Type", "null");
      addOption(testTypeSelect, "Obstetric ultrasound", "Obstetric ultrasound");
      addOption(
        testTypeSelect,
        "Transvaginal ultrasound",
        "Transvaginal ultrasound"
      );
      addOption(testTypeSelect, "Bone ultrasound", "Bone ultrasound");

      break;
    default:
      testTypeDiv.style.display = "block";
      break;
  }
}

function addOption(select, text, value) {
  var option = document.createElement("option");
  option.text = text;
  option.value = value;
  select.add(option);
}
  // Fetch doctors based on the selected surgery type
  function fetchDoctorsBySurgeryType() {
    var selectedSurgeryType = document.getElementById("SurgeryType").value;

    // Make an AJAX request to your server to fetch doctors based on the selected surgery type
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/get_doctors", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Populate the doctors dropdown with the received data
            var doctorsDropdown = document.getElementById("DoctorName");
            doctorsDropdown.innerHTML = '<option value="">Select a Doctor</option>';
            var doctorsData = JSON.parse(xhr.responseText);
            for (var i = 0; i < doctorsData.length; i++) {
                doctorsDropdown.innerHTML += '<option value="' + doctorsData[i][5] + '">Dr. ' + doctorsData[i][5] + '</option>';
               
            }
        }
    };
    xhr.send("SurgeryType=" + selectedSurgeryType);
}

// Attach an event listener to the SurgeryType dropdown
document.getElementById("SurgeryType").addEventListener("change", fetchDoctorsBySurgeryType);
   // Validate input to allow only two-digit numbers (hours)
document.getElementById("appointmentHour").addEventListener("input", function () {
this.value = this.value.replace(/[^0-9]/g, ''); // Remove non-numeric characters
if (this.value.length > 2) {
    this.value = this.value.substring(0, 2); // Limit to two characters
}
});
document.getElementById("SurgeryType").addEventListener("change", fetchDoctorsBySurgeryType);
   // Validate input to allow only two-digit numbers (hours)
document.getElementById("appointmentHour1").addEventListener("input", function () {
this.value = this.value.replace(/[^0-9]/g, ''); // Remove non-numeric characters
if (this.value.length > 2) {
    this.value = this.value.substring(0, 2); // Limit to two characters
}
});