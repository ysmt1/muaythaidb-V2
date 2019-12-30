$(document).ready(function () {

    $('#hideRows').change(function () {
        var isChecked = !this.checked;

        $("#indexTable tr td:contains('No Ratings')").each(function (index, element) {
            $(this).parent("tr").toggleClass("hide");
        });
        reapplyStripes()
    });

    $("#filterRow").keyup(function () {
        var value = this.value.toLowerCase().trim();

        $("#indexTable tr").not(".hide").each(function (index) {
            if (!index) return;
            $(this).find("td.searchable").each(function () {
                var id = $(this).text().toLowerCase().trim();
                var not_found = (id.indexOf(value) == -1);
                $(this).closest('tr').toggle(!not_found);
                return not_found;
            });
        });
        reapplyStripes()
    });

    $('th').click(function () {
        var icon = $(this).find('span.sort-icon')
        icon.html('<i class="fas fa-sort-up"></i>')
        var table = $(this).parents('table').eq(0)
        var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()))
        this.asc = !this.asc
        if (!this.asc) {
            rows = rows.reverse()
            icon.html('<i class="fas fa-sort-down"></i>')
        }
        for (var i = 0; i < rows.length; i++) {
            table.append(rows[i])
        }
        reapplyStripes()
    })
    function comparer(index) {
        return function (a, b) {
            var valA = getCellValue(a, index), valB = getCellValue(b, index)
            return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
        }
    }
    function getCellValue(row, index) { return $(row).children('td').eq(index).text() }

    function reapplyStripes() {
        $("#indexTable tr:visible").each(function (index) {
            $(this).css("background-color", !!(index & 1) ? "rgba(0,0,0,0)" : "rgba(0,0,0,0.05)");
        });
    }
});
