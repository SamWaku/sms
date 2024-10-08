document.addEventListener("DOMContentLoaded", function () {
  function fetchStudents(group) {
    console.log(`Fetching students for group: ${group}`);
    // Update the heading with the selected group name
    document.getElementById("group-name-heading").textContent = group;

    fetch(`/get-students-group?group=${encodeURIComponent(group)}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Data received:", data); // Log the data received
        const tbody = document.getElementById("students-table-body");
        tbody.innerHTML = ""; // Clear existing content
        if (data.length === 0) {
          tbody.innerHTML = "<tr><td colspan='9'>No students found</td></tr>";
        } else {
          data.forEach((student) => {
            const currentCourses = student.current_courses.join(", ");
            const repeatedCourses = student.repeated_courses.join(", ");
            tbody.innerHTML += `
              <tr>
                <td>${student.student_number}</td>
                <td>${student.first_name}</td>
                <td>${student.last_name}</td>
                <td>${student.email}</td>
                <td>${student.school}</td>
                <td>${currentCourses}</td>
                <td>${repeatedCourses}</td>
                <td>${student.field_of_study}</td>
                <td>${student.year}</td>
              </tr>`;
          });
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error); // Log any errors
        const tbody = document.getElementById("students-table-body");
        tbody.innerHTML =
          "<tr><td colspan='9'>Error loading students</td></tr>";
      });
  }

  // Attach event listeners to dropdown items
  document.querySelectorAll(".dropdown-item").forEach((item) => {
    item.addEventListener("click", function () {
      fetchStudents(this.textContent.trim());
    });
  });
});

// function fetchStudents(group) {
//   fetch(`/get-students-group?group=${encodeURIComponent(group)}`)
//     .then((response) => response.json())
//     .then((data) => {
//       const tbody = document.getElementById("students-table-body");
//       tbody.innerHTML = "";
//       if (data.length === 0) {
//         tbody.innerHTML = "<tr><td colspan='9'>No students found</td></tr>";
//       } else {
//         data.forEach((student) => {
//           const currentCourses = student.current_courses.join(", ");
//           const repeatedCourses = student.repeated_courses.join(", ");
//           tbody.innerHTML += `
//             <tr>
//               <td>${student.student_number}</td>
//               <td>${student.first_name}</td>
//               <td>${student.last_name}</td>
//               <td>${student.email}</td>
//               <td>${student.school}</td>
//               <td>${currentCourses}</td>
//               <td>${repeatedCourses}</td>
//               <td>${student.field_of_study}</td>
//               <td>${student.year}</td>
//             </tr>`;
//         });
//       }
//     })
//     .catch((error) => {
//       console.error("Error fetching data:", error);
//       const tbody = document.getElementById("students-table-body");
//       tbody.innerHTML = "<tr><td colspan='9'>Error loading students</td></tr>";
//     });
// }

// function fetchStudents(group) {
//   fetch(`/get-students-group?group=${encodeURIComponent(group)}`)
//     .then((response) => response.json())
//     .then((data) => {
//       const tbody = document.getElementById("students-table-body");
//       tbody.innerHTML = "";
//       if (data.length === 0) {
//         tbody.innerHTML = "<tr><td colspan='9'>No students found</td></tr>";
//       } else {
//         data.forEach((student) => {
//           const currentCourses = student.current_courses.join(", ");
//           const repeatedCourses = student.repeated_courses.join(", ");
//           tbody.innerHTML += `
//             <tr>
//               <td>${student.student_number}</td>
//               <td>${student.first_name}</td>
//               <td>${student.last_name}</td>
//               <td>${student.email}</td>
//               <td>${student.school}</td>
//               <td>${currentCourses}</td>
//               <td>${repeatedCourses}</td>
//               <td>${student.field_of_study}</td>
//               <td>${student.year}</td>
//             </tr>`;
//         });
//       }
//     })
//     .catch((error) => {
//       console.error("Error fetching data:", error);
//       const tbody = document.getElementById("students-table-body");
//       tbody.innerHTML = "<tr><td colspan='9'>Error loading students</td></tr>";
//     });
// }

// document.addEventListener("DOMContentLoaded", () => {
//   document
//     .getElementById("group-dropdown")
//     .addEventListener("click", function (event) {
//       const group = event.target.textContent;
//       fetchStudents(group);
//     });
// });

// function fetchStudents(group) {
//   fetch(`/get-students-group?group=${group}`)
//     .then((response) => response.json())
//     .then((data) => {
//       const tbody = document.getElementById("students-table-body");
//       tbody.innerHTML = "";
//       data.forEach((student) => {
//         tbody.innerHTML += `
//                       <tr>
//                           <td>${student.student_number}</td>
//                           <td>${student.first_name}</td>
//                           <td>${student.last_name}</td>
//                           <td>${student.email}</td>
//                           <td>${student.school}</td>
//                           <td>${student.field_of_study}</td>
//                           <td>${student.year}</td>
//                       </tr>`;
//       });
//     });
// }

// document.addEventListener("DOMContentLoaded", () => {
//   document
//     .getElementById("group-dropdown")
//     .addEventListener("click", function (event) {
//       const group = event.target.textContent;
//       fetchStudents(group);
//     });
// });

// function fetchStudents(group) {
//   fetch(`/get-students-group?group=${group}`)
//     .then((response) => response.json())
//     .then((data) => {
//       const tbody = document.getElementById("students-table-body");
//       tbody.innerHTML = "";
//       data.forEach((student) => {
//         tbody.innerHTML += `
//                     <tr>
//                         <td>${student.student_number}</td>
//                         <td>${student.first_name}</td>
//                         <td>${student.last_name}</td>
//                         <td>${student.email}</td>
//                         <td>${student.field_of_study__name}</td>
//                         <td>${student.gpa}</td>
//                         <td>${student.year__name}</td>
//                     </tr>`;
//       });
//     });
// }

// document.addEventListener('DOMContentLoaded', () => {
//     document.getElementById('year-dropdown').addEventListener('click', function(event) {
//         const year = event.target.textContent;
//         fetchFields(year);
//     });

//     document.getElementById('field-list').addEventListener('click', function(event) {
//         const year = document.getElementById('year-dropdown').dataset.selectedYear;
//         const field = event.target.textContent;
//         loadStudents(year, field);
//     });
// });

// function fetchFields(year) {
//     fetch(`/get-fields/?year=${year}`)
//         .then(response => response.json())
//         .then(fields => {
//             const fieldDropdown = document.getElementById('field-list');
//             fieldDropdown.innerHTML = '';
//             fields.forEach(field => {
//                 fieldDropdown.innerHTML += `<li class="dropdown-item">${field}</li>`;
//             });
//             document.getElementById('dropdownMenuButton2').disabled = false;
//             document.getElementById('year-dropdown').dataset.selectedYear = year;
//         });
// }

// function loadStudents(year, field) {
//     fetch(`/get-students/?year=${year}&field=${field}`)
//         .then(response => response.json())
//         .then(data => {
//             const studentsTableBody = document.getElementById('students-table-body');
//             studentsTableBody.innerHTML = '';
//             data.forEach(student => {
//                 studentsTableBody.innerHTML += `
//                     <tr>
//                         <td>${student.student_number}</td>
//                         <td>${student.first_name}</td>
//                         <td>${student.last_name}</td>
//                         <td>${student.email}</td>
//                         <td>${student.field_of_study}</td>
//                         <td>${student.gpa}</td>
//                         <td>${student.year}</td>
//                     </tr>`;
//             });
//         });
// }
