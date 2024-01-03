function updateDoctors() {
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
        doctorsDropdown.innerHTML +=
          '<option value="' +
          doctorsData[i][5] +
          '">Dr. ' +
          doctorsData[i][5] +
          "</option>";
      }
    }
  };
  xhr.send("SurgeryType=" + selectedSurgeryType);
}

// Attach an event listener to the SurgeryType dropdown
document
  .getElementById("SurgeryType")
  .addEventListener("change", fetchDoctorsBySurgeryType);
// Validate input to allow only two-digit numbers (hours)
document
  .getElementById("appointmentHour")
  .addEventListener("input", function () {
    this.value = this.value.replace(/[^0-9]/g, ""); // Remove non-numeric characters
    if (this.value.length > 2) {
      this.value = this.value.substring(0, 2); // Limit to two characters
    }
  });
document
  .getElementById("SurgeryType")
  .addEventListener("change", fetchDoctorsBySurgeryType);
// Validate input to allow only two-digit numbers (hours)
document
  .getElementById("appointmentHour1")
  .addEventListener("input", function () {
    this.value = this.value.replace(/[^0-9]/g, ""); // Remove non-numeric characters
    if (this.value.length > 2) {
      this.value = this.value.substring(0, 2); // Limit to two characters
    }
  });
