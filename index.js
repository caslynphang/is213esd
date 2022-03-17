

$(document).ready(function(){
    
    $("#submit").click(function(){
        var stockName = $("#stockName").val();
        console.log(stockName);

        url = "http://127.0.0.1:5000/stock_info/buy/"

        url = url + stockName.toUpperCase()
        
        axios.get(url, {
            params: {
                stockName: stockName,
            }
        })
    
        .then(response => {
            console.log(response.data);
        })
    
        .catch(error => {
            console.log(error.message);
        })

    });

});