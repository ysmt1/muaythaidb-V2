$(document).ready(function () {

    var icon;
    const regions = {
        'North': ['Chiang Mai', 'Lampang', 'Pai'],
        'NorthEast': ['Ubon Ratchathani', 'Buriram', 'Khlong Phai'],
        'Central': ['Bangkok', 'Nonthaburi', 'Pathum Thani'],
        'East': ['Pattaya'],
        'West': ['Hua Hin'],
        'South': ['Phuket', 'Koh Phangan', 'Koh Samui', 'Krabi']
    }

    // Reapply zebra striping
    function reapplyStripes() {
        $("#indexTable tr:visible").each(function (index) {
            $(this).css("background-color", !!(index & 1) ? "rgba(0,0,0,0)" : "rgba(0,0,0,0.05)");
        });
    }

    function comparer(index, desc) {
        return function (a, b) {
            var valA = getCellValue(a, index),
                valB = getCellValue(b, index)
            var result = $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB);
            // If desc is set we sort descending otherwise ascending by default.
            if (desc) {
                result *= -1;
                icon.html('<i class="fas fa-sort-down"></i>')
            }
            return result;
        }
    }
    function getCellValue(row, index) {
        var cellValue = $(row).children('td').eq(index).text().trim()
        if (cellValue === "No Ratings") {
            return "0"
        }
        return cellValue
    }

    // Table sorting function
    $('th').click(function () {
        icon = $(this).find('span.sort-icon')
        icon.html('<i class="fas fa-sort-up"></i>')
        var table = $(this).parents('table').eq(0)
        this.asc = !this.asc
        var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index(), !this.asc))
        for (var i = 0; i < rows.length; i++) {
            table.append(rows[i])
        }
        reapplyStripes()
    })

    // Table searching function
    $("#filterRow").keyup(function () {
        var value = $(this).val().toLowerCase().trim();

        $("#indexTable tbody tr").not(".filterHide").each(function (index) {

            var row = $(this);
            var gymName = row.find('td').eq(0).text().toLowerCase().trim();
            var city = row.find('td').eq(1).text().toLowerCase().trim();

            if (gymName.indexOf(value) == -1 && city.indexOf(value) == -1) {
                row.hide().addClass('searchHide');
            }
            else {
                row.show().removeClass('searchHide');
            }

        });
        reapplyStripes();
    });

    // Table checkbox filters function
    $("input[type='checkbox']").change(function () {
        var classes = [];
        var hideNoReviews = false;

        $("input[type='checkbox']").each(function () {
            if ($(this).is(":checked")) {
                classes.push($(this).attr('id'));
            }
        })

        var hideIndex = classes.indexOf('hideRows');
        if (hideIndex > -1) {
            hideNoReviews = true;
            classes.splice(hideIndex, 1);
        }
        cities = classes.map(function (i) { return i.replace('region', '') })
            .map(function (i) { return regions[i].join(); }).join().split(",");

        if (cities == "" && !hideNoReviews) { // if no filters selected, show all items
            $("#indexTable tbody tr").not(".searchHide").show().removeClass('filterHide');
            reapplyStripes()
        } else { // otherwise, hide everything...
            $("#indexTable tbody tr").not(".searchHide").hide().addClass('filterHide');
            $("#indexTable tbody tr").not(".searchHide").each(function () {
                var show = false;
                var row = $(this);

                if (hideNoReviews) {
                    if (row.find('td').eq(2).text().trim() == "No Ratings") {
                        show = false;
                    } else {
                        show = true;
                        if (cities != "") {
                            cities.forEach(function (city) {
                                if (row.find('td').eq(1).text() != city) {
                                    show = false;
                                }
                            });
                        }
                    }
                }

                cities.forEach(function (city) {
                    if (row.find('td').eq(1).text() == city) {
                        show = true;
                        if (hideNoReviews && row.find('td').eq(2).text().trim() == "No Ratings") {
                            show = false;
                        }
                    }
                })
                if (show) {
                    row.show().removeClass('filterHide');
                }
            })
            reapplyStripes()
        }
    })
})