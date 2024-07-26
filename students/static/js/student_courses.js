document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("group-dropdown")
    .addEventListener("click", function (event) {
      const group = event.target.textContent;
      fetchStudents(group);
    });
});

function fetchStudents(group) {
  fetch(`/get-students-group?group=${group}`)
    .then((response) => response.json())
    .then((data) => {
      const tbody = document.getElementById("students-table-body");
      tbody.innerHTML = "";
      data.forEach((student) => {
        tbody.innerHTML += `
                      <tr>
                          <td>${student.student_number}</td>
                          <td>${student.first_name}</td>
                          <td>${student.last_name}</td>
                          <td>${student.email}</td>
                          <td>${student.school}</td>
                          <td>${student.field_of_study}</td>
                          <td>${student.year}</td>
                      </tr>`;
      });
    });
}

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
