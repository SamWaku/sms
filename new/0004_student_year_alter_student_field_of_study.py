# Generated by Django 5.0.6 on 2024-06-06 10:33

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0003_academicyear_fieldofstudy"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="year",
            field=models.ForeignKey(
                default=django.utils.timezone.now,
                on_delete=django.db.models.deletion.CASCADE,
                to="students.academicyear",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="student",
            name="field_of_study",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="students.fieldofstudy"
            ),
        ),
    ]


{% extends "students/base.html" %}

{% block body %}
<div class="dropdown">
    <button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
      Select Year
    </button>
    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton" id="year-dropdown">
      {% for year, fields in grouped_students.items %}
        <li class="dropdown-item dropdown-header">{{ year }}</li>
      {% endfor %}
    </ul>
</div>

<div class="dropdown" id="field-dropdown">
  <button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton2" data-bs-toggle="dropdown" aria-expanded="false" disabled>
    Select Field of Study
  </button>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton2" id="field-list">
    <!-- Field of study options will be loaded dynamically based on the selected year -->
  </ul>
</div>

<div id="students-list">
  <!-- Student list will be loaded dynamically based on the selected year and field of study -->
</div>

<script>
  // Function to load field of study options based on the selected year
  function loadFields(year) {
    fetch('/get-fields/?year=' + year)
      .then(response => response.json())
      .then(data => {
        const fieldDropdown = document.getElementById('field-list');
        fieldDropdown.innerHTML = '';
        data.forEach(field => {
          fieldDropdown.innerHTML += `<li class="dropdown-item">${field}</li>`;
        });
        document.getElementById('dropdownMenuButton2').disabled = false;
      });
  }

  // Function to load students based on the selected year and field of study
  function loadStudents(year, field) {
    fetch(`/get-students/?year=${year}&field=${field}`)
      .then(response => response.json())
      .then(data => {
        const studentsList = document.getElementById('students-list');
        studentsList.innerHTML = '';
        data.forEach(student => {
          studentsList.innerHTML += `<div>${student.first_name} ${student.last_name}</div>`;
        });
      });
  }

  // Event listener for year selection
  document.getElementById('year-dropdown').addEventListener('click', function(event) {
    const year = event.target.textContent;
    loadFields(year);
  });

  // Event listener for field of study selection
  document.getElementById('field-list').addEventListener('click', function(event) {
    const year = document.getElementById('year-dropdown').textContent;
    const field = event.target.textContent;
    loadStudents(year, field);
  });
</script>
{% endblock %}


