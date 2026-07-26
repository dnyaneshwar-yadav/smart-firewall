// =====================================
// Smart Firewall Analytics
// Optimized Version
// =====================================

let actionChart = null;
let protocolChart = null;


// =====================================
// Create Charts
// =====================================

function createCharts(data) {

    actionChart = new Chart(

        document.getElementById("actionChart"),

        {

            type: "pie",

            data: {

                labels: data.action_data.map(x => x[0]),

                datasets: [{

                    data: data.action_data.map(x => x[1])

                }]

            }

        }

    );



    protocolChart = new Chart(

        document.getElementById("protocolChart"),

        {

            type: "bar",

            data: {

                labels: data.protocol_data.map(x => x[0]),

                datasets: [{

                    label: "Packets",

                    data: data.protocol_data.map(x => x[1])

                }]

            }

        }

    );

}


// =====================================
// Update Charts
// =====================================

function updateCharts(data){

    // ---------- Action Chart ----------

    actionChart.data.labels =
        data.action_data.map(x => x[0]);

    actionChart.data.datasets[0].data =
        data.action_data.map(x => x[1]);

    actionChart.update();



    // ---------- Protocol Chart ----------

    protocolChart.data.labels =
        data.protocol_data.map(x => x[0]);

    protocolChart.data.datasets[0].data =
        data.protocol_data.map(x => x[1]);

    protocolChart.update();

}


// =====================================
// Fetch Analytics
// =====================================

async function updateAnalytics(){

    try{

        const response =
            await fetch("/analytics-data");

        const data =
            await response.json();


        // Cards

        document.getElementById("analytics_total_packets").innerText =
            data.total_packets;

        document.getElementById("analytics_allowed_packets").innerText =
            data.allowed_packets;

        document.getElementById("analytics_blocked_packets").innerText =
            data.blocked_packets;

        document.getElementById("analytics_total_rules").innerText =
            data.total_rules;


        // Charts

        if(actionChart == null){

            createCharts(data);

        }

        else{

            updateCharts(data);

        }

    }

    catch(error){

        console.log(error);

    }

}


// First Load

updateAnalytics();


// Refresh Every 5 Seconds

setInterval(updateAnalytics, 5000);
