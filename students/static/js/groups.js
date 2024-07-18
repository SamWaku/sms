document.addEventListener("DOMContentLoaded", function () {
  const yearDropdown = document.getElementById("year-dropdown");
  const fieldDropdownButton = document.getElementById("fieldDropdownButton");
  const fieldDropdownMenu = document.getElementById("field-list");
  const studentsTableBody = document.getElementById("students-table-body");

  yearDropdown.addEventListener("click", function (event) {
    const year = event.target.getAttribute("data-year");
    if (year) {
      fetchFields(year);
    }
  });

  fieldDropdownMenu.addEventListener("click", function (event) {
    const field = event.target.getAttribute("data-field");
    const year = fieldDropdownButton.getAttribute("data-year");
    if (field && year) {
      fetchStudents(year, field);
    }
  });

  function fetchFields(year) {
    fetch(`/get_fields_student/?year=${year}`)
      .then((response) => response.json())
      .then((data) => {
        fieldDropdownButton.disabled = false;
        fieldDropdownButton.setAttribute("data-year", year);
        fieldDropdownMenu.innerHTML = "";
        data.forEach((field) => {
          const li = document.createElement("li");
          li.innerHTML = `<a class="dropdown-item" href="#" data-field="${field}">${field}</a>`;
          fieldDropdownMenu.appendChild(li);
        });
      });
  }

  function fetchStudents(year, field) {
    fetch(`/get_students_group/?year=${year}&field=${field}`)
      .then((response) => response.json())
      .then((data) => {
        studentsTableBody.innerHTML = "";
        data.forEach((student) => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
                        <td>${student.student_number}</td>
                        <td>${student.first_name}</td>
                        <td>${student.last_name}</td>
                        <td>${student.email}</td>
                        <td>${student.school}</td>
                        <td>${student.field_of_study}</td>
                        <td>${student.year}</td>
                    `;
          studentsTableBody.appendChild(tr);
        });
      });
  }
});
