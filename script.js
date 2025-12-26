// This function is triggered from the dashboard page
function loadStats() {
    let damage = $("#damageFilter").val();

    $.ajax({
        url: "/get_stats",
        method: "POST",
        data: { damage: damage },
        success: function(response) {
            $("#totalCars").text(response.cars_count);
            $("#averagePrice").text(response.avg_price);
            $("#chart").attr("src", response.chart_url).show();
        }
    });
}
