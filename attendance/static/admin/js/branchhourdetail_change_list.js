// document.addEventListener("DOMContentLoaded", function () {
//     setTimeout(function () {
//         const tableRows = document.querySelectorAll(".result_row");
//         for (const row of tableRows) {
//             const cells = row.querySelectorAll("td");
//             let hasNullValue = false;
//             let finishedMarkingCheckbox = row.querySelector("input[type='checkbox']");

//             for (const cell of cells) {
//                 if (cell.textContent.trim() === "-") {
//                     hasNullValue = true;
//                     break;
//                 }
//             }

//             if (!hasNullValue && finishedMarkingCheckbox.checked) {
//                 // No null values and checkbox checked, don't color
//                 continue;
//             }

//             row.classList.add("colored-row");  // Add the class for coloring
//         }
//     }, 100);

// });
