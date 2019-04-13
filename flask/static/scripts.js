// var r1 = 255, g1 = 60, b1 = 60;
// var r2 = 60, g2 = 255, b2 = 60;
// var color1, color2, color3;
// var color4, color5, color6;
// var gradient1, gradient2, gradient3, gradient4;

// setInterval(function () {
//     if (r1 > 60 && b1 == 60) {
//         r1--;
//         g1++;
//     }
//     if (g1 > 60 && r1 == 60) {
//         g1--;
//         b1++;
//     }
//     if (b1 > 60 && g1 == 60) {
//         r1++;
//         b1--;
//     }
//     if (r2 > 60 && b2 == 60) {
//         r2--;
//         g2++;
//     }
//     if (g2 > 60 && r2 == 60) {
//         g2--;
//         b2++;
//     }
//     if (b2 > 60 && g2 == 60) {
//         r2++;
//         b2--;
//     }
//     color1 = "rgba(" + r1 + ", " + g1 + ", " + b1 + ", 0.2)";
//     color2 = "rgba(" + g1 + ", " + b1 + ", " + r1 + ", 0.4)";
//     color3 = "rgba(" + b1 + ", " + r1 + ", " + g1 + ", 0.6)";
//     color4 = "rgba(" + r2 + ", " + g2 + ", " + b2 + ", 0.6)";
//     color5 = "rgba(" + g2 + ", " + b2 + ", " + r2 + ", 0.6)";
//     color6 = "rgba(" + b2 + ", " + r2 + ", " + g2 + ", 0.6)";

//     gradient3 = "linear-gradient(20deg, " + color1 + ", " + color2 + ", " + color3 + " 120%)";
//     gradient4 = "linear-gradient(150deg, " + color2 + ", " + color3 + ", " + color1 + " 60%)";
//     gradient5 = "linear-gradient(190deg, " + color4 + ", " + color5 + ", " + color6 + " 30%)";
//     gradient6 = "linear-gradient(230deg, " + color5 + ", " + color6 + ", " + color4 + " 30%)";

//     document.body.style.background = (gradient3 + ", " + gradient4 + ", " + gradient5 + ", " + gradient6);
// }, 400);

// d3.text("./static/data.tsv", function (data) {
//     var parsedTSV = d3.tsv.parseRows(data);
//     // console.log(parsedCSV);

//     d3.select("tbody").remove();

//     d3.select("table")
//         .append("tbody")

//         .selectAll("tr")
//         .data(parsedTSV).enter()
//         .append("tr")

//         .selectAll("td")
//         .data(function (d) { return d; }).enter()
//         .append("td")
//         .text(function (d) { return d; });
// });

// setInterval(function () {

//     var myHeaders = new Headers();
//     myHeaders.append('pragma', 'no-cache');
//     myHeaders.append('cache-control', 'no-cache');

//     var myInit = {
//         method: 'GET',
//         headers: myHeaders,
//     };

//     var myRequest = new Request('/static/data.tsv');

//     fetch(myRequest, myInit).then(function (response) {
//         response.text().then(function (text) {

//             // console.log(text);

//             var parsedTSV = d3.tsv.parseRows(text);
//             console.log(parsedTSV);

//             d3.select("tbody").remove();

//             d3.select("table")
//                 .append("tbody")

//                 .selectAll("tr")
//                 .data(parsedTSV).enter()
//                 .append("tr")

//                 .selectAll("td")
//                 .data(function (d) { return d; }).enter()
//                 .append("td")
//                 .text(function (d) { return d; });
//         });
//     });
// }, 3000);