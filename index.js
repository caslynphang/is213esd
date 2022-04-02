// 1. Needed for jQuery to work in external file
$(document).ready(function(){
    

//************************ SUBMIT BUTTON LOGIC ******************************************

    //2. Use JQuery to select submit button element 
    $("#submit").click(function(){

        //3. Extract stock name entered into field
        var stockName = $("#stockName").val();

        //4. preparing url for GET Axios call to stockinfo.py
        url = "http://127.0.0.1:5000/stock_info/buy/"

        url = url + stockName.toUpperCase()
        
        //5. axios call to stockinfo.py
        axios.get(url, {
            params: {
            }
        })
    
        .then(response => {

            //6. split response into its ticker and price
            var ticker = response.data.Ticker.toUpperCase();
            var price = response.data['Close Price'];
            
            //7. appending ticker and price into buy info section
            $("#ticker").text(ticker);
            $("#price").text("USD " + price);

            //8. showing buy info
            $("#buy_info").show()

        //************************ BUY BUTTON LOGIC ******************************************

        //9. Function if user clicks buy
        $("#buy").click(function(){

            console.log("clicked");

            //11. preparing url for POST Axios call to place_order.py
            url = "http://127.0.0.1:5001/place_order/buy";

            // console.log(url);

            axios.post(url, {
                // Used Dummy data first, need to extract from user input
                params: {
                    "ticker": "TSLA",
                    "price": 800.5,
                    "quantity:": 5,
                    "order_type": "buy",
                    "portfolio_id": 1
                }
            })
            
            .then(response => {
                console.log(response.data);
            })
            
            .catch(error => {
                console.log(error.message);
            })

        })

        //************************ BUY BUTTON LOGIC ******************************************

        })
    
        .catch(error => {
            console.log(error.message);
        })

    });

//************************ SUBMIT BUTTON LOGIC ******************************************

});